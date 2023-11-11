from vakt.rules import Eq, Truthy
import vakt

from src.authentication.constants import ACCESS_TOKEN
from src.authentication.exceptions import *
from src.authentication.service import AuthenticationService
from src.authorization.config import StorageABAC
from src.authorization.const import SECURITY, TOKEN_SECURITY
from src.authorization.exceptions import *
from src.authorization.checkers import *
from src.authorization.informants import *
from src.authorization.schemas import *
from src.config import SchemaAPI
from src.const import SUPPORT_SECURITY_OWNER
from src.database.exceptions import DBException
from src.database.models.others.vakt_policy import VaktPolicy
from src.schemas.message import MessageSchema
from src.services.unit_of_work import IUnitOfWork


class AuthorizationService:
    def __init__(
        self,
        uow: IUnitOfWork,
        authenticate_service: AuthenticationService,
        resource_InformantService: IResourceInformantService,
        action_InformantService: IActionInformantService,
        subject_InformantService: ISubjectInformantService,
    ):
        self.__uow = uow
        self.__authenticate_service = authenticate_service
        self.__checkers: list[BaseCheckerAuthService] = [
            RoleCheckerAuthService(),
            RoleOwnerCheckerAuthService(),
        ]
        self.__resource_InformantService = resource_InformantService
        self.__action_InformantService = action_InformantService
        self.__subject_InformantService = subject_InformantService

    async def __restore_policies(self):
        try:
            async with self.__uow:
                for policy in await self.__uow.policies.get_all():
                    s = []
                    for sub in policy.subjects:
                        new_sub = {"role_id": Eq(sub["role_id"])}
                        if "is_owner" in sub:
                            new_sub["is_owner"] = Truthy()
                        s.append(new_sub)

                    a = [{"name": Eq(a["name"])} for a in policy.actions]
                    r = [{"name": Eq(r["name"])} for r in policy.resources]
                    p = vakt.Policy(
                        policy.id,
                        actions=a,
                        resources=r,
                        subjects=s,
                        effect=vakt.ALLOW_ACCESS,
                        description=policy.description,
                    )
                    StorageABAC.delete(p.uid)
                    StorageABAC.add(p)
        except DBException as db_e:
            raise DBAuthorizationException(db_e.message) from db_e

    async def check_authorization(
        self, action: str, resource: ResourceData, token: str
    ):
        try:
            ps = StorageABAC.retrieve_all()
            ps = [p for p in ps]
            if len(ps) == 0:
                await self.__restore_policies()

            token_data = self.__authenticate_service.decode_token(token, ACCESS_TOKEN)
            async with self.__uow:
                subject_data = await self.__subject_InformantService.get(token_data)
                if not resource.id:
                    resource.id = subject_data.id

                resource_data = await self.__resource_InformantService.get(
                    resource, self.__uow
                )
                action_data = await self.__action_InformantService.get(action)

                for checker in self.__checkers:
                    result: StatusAccess = checker.check(
                        action_data, resource_data, subject_data
                    )
                    if result.value:
                        return resource_data, subject_data
                raise NoAccessAuthorizationException()
        except DBException as db_e:
            raise DBAuthorizationException(db_e.message) from db_e

    async def get_all_methods(self):
        security_methods = []
        for path, methods in SchemaAPI.schema["paths"].items():
            for rest_m, m in methods.items():
                if SECURITY in m:
                    f = False
                    for s in m[SECURITY]:
                        if TOKEN_SECURITY in s:
                            f = True
                            break
                    if f:
                        security_methods.append(
                            {
                                "is_owner": SUPPORT_SECURITY_OWNER in m["summary"],
                                "description": m["summary"],
                                "id": m["operationId"],
                                "tag": m["tags"][0],
                                "resource": path,
                                "action": rest_m,
                            }
                        )
        return security_methods

    async def get_all_policies(self, action: str, resource: str):
        policies = []
        for p in StorageABAC.retrieve_all(100):
            is_finded_action = False
            is_finded_resource = False
            for a in p.actions:
                v = a.get("name", None)
                if v and v.val == action:
                    is_finded_action = True
                    break

            if is_finded_action:
                for r in p.resources:
                    v = r.get("name", None)
                    if v and v.val == resource:
                        is_finded_resource = True
                        break

            if is_finded_action and is_finded_resource:
                subjects = []
                for s in p.subjects:
                    sub = {"role_id": s["role_id"].val}
                    if "is_owner" in s:
                        sub["is_owner"] = True
                    subjects.append(sub)
                policies.append(
                    {"uid": p.uid, "description": p.description, "subjects": subjects}
                )
        return policies

    async def update_policy(self, data: UpdatePolicySchema):
        try:
            async with self.__uow:
                policy = StorageABAC.get(data.uid)
                subjects = []
                for s in data.subjects:
                    sub = {"role_id": Eq(s.role_id)}
                    if s.is_owner:
                        sub["is_owner"] = Truthy()
                    subjects.append(sub)

                policy.subjects = subjects
                policy.description = data.description
                StorageABAC.update(policy)

                policy_db = await self.__uow.policies.get_by_id(data.uid)

                s = []
                for sub in policy.subjects:
                    new_sub = {"role_id": sub["role_id"].val}
                    if "is_owner" in sub:
                        new_sub["is_owner"] = True
                    s.append(new_sub)

                r = [{"name": r["name"].val} for r in policy.resources]
                a = [{"name": a["name"].val} for a in policy.actions]
                if policy_db:
                    policy_db.description = data.description
                    policy_db.subjects = s
                    policy_db.resources = r
                    policy_db.actions = a
                else:
                    policy_db = VaktPolicy(
                        id=data.uid,
                        description=data.description,
                        subjects=s,
                        resources=r,
                        actions=a,
                    )
                    await self.__uow.policies.add(policy_db)
                # await self.__uow.policies.delete(id=data.uid)
                await self.__uow.commit()
            return MessageSchema(message="Политика успешно изменена")
        except DBException as db_e:
            raise DBAuthorizationException(db_e.message) from db_e
