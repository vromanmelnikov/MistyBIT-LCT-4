from vakt import Guard, RulesChecker
from vakt.storage.redis import RedisStorage
from vakt import MemoryStorage

from src.authorization.const import POLICIES_COLLECTION_NAME
from src.authorization.policies import policies
from src.config import SyncRedisConnection
from src.database.models.others.vakt_policy import VaktPolicy
from src.dependies import create_uow


StorageABAC = RedisStorage(SyncRedisConnection, collection=POLICIES_COLLECTION_NAME)
# StorageABAC = MemoryStorage()


async def init_default_policies():
    for policy in policies:
        StorageABAC.delete(policy.uid)
        StorageABAC.add(policy)
    uow = create_uow()
    async with uow:
        for p in policies:
            s = []
            for sub in p.subjects:
                new_sub = {"role_id": sub["role_id"].val}
                if "is_owner" in sub:
                    new_sub["is_owner"] = True
                s.append(new_sub)
                
            r = [{"name": r["name"].val} for r in p.resources]
            a = [{"name": a["name"].val} for a in p.actions]
            policy_db = VaktPolicy(
                id=p.uid,
                description=p.description,
                subjects=s,
                resources=r,
                actions=a,
            )
            p_in_db = await uow.policies.get_by_id(p.uid)
            if p_in_db:
                await uow.policies.delete(id=p.uid)
            await uow.policies.add(policy_db)
        await uow.commit()


ABACGuard = Guard(StorageABAC, RulesChecker())
