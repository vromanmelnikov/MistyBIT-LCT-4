from abc import ABC, abstractmethod
from vakt import Inquiry

from src.authorization.config import ABACGuard
from src.authorization.schemas import *


def subject_build_role(subject: SubjectData):
    return {"role_id": subject.role_id}


def resource_build_name(resource: ResourceData):
    return {"name": resource.name}


def action_build_name(action: ActionData):
    return {"name": action.name}


class BaseCheckerAuthService(ABC):
    @abstractmethod
    def check(self, action: ActionData, resource: ResourceData, subject: SubjectData):
        raise NotImplementedError()

    def _build_inq_and_execute(self, action, resource, subject):
        inq = Inquiry(action=action, resource=resource, subject=subject)
        return StatusAccess.allow if ABACGuard.is_allowed(inq) else StatusAccess.denied


class RoleCheckerAuthService(BaseCheckerAuthService):
    def check(self, action: ActionData, resource: ResourceData, subject: SubjectData):
        subject_inq = subject_build_role(subject)
        resource_inq = resource_build_name(resource)
        action_inq = action_build_name(action)
        return self._build_inq_and_execute(action_inq, resource_inq, subject_inq)

class RoleOwnerCheckerAuthService(BaseCheckerAuthService):
    def check(self, action: ActionData, resource: ResourceData, subject: SubjectData):
        subject_inq = subject_build_role(subject)
        resource_inq = resource_build_name(resource)
        action_inq = action_build_name(action)
        if subject and subject.id and resource and resource.owner_id:
            subject_inq["is_owner"] = subject.id == resource.owner_id
        return self._build_inq_and_execute(action_inq, resource_inq, subject_inq)