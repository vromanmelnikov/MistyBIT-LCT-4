from src.database.models import *
from src.mappers import SimpleMapper
from src.user.schemas import *


class RoleMapper(SimpleMapper[RoleSchema]):
    def __init__(self):
        super().__init__(RoleSchema)


class UserDBMapper(SimpleMapper[UserDBSchema]):
    def __init__(self):
        super().__init__(UserDBSchema)

    def create_from_input(self, user: CreateUserSchema):
        return User(
            email=user.email,
            hashed_password=user.password,
            role_id=user.role_id,
            firstname=user.firstname,
            lastname=user.lastname,
            patronymic=user.patronymic,
        )


class ManagerMapper(SimpleMapper[ManagerSchema]):
    def __init__(self):
        super().__init__(ManagerSchema)

    def create_from_input(self, user: CreateUserSchema):
        user_db = UserDBMapper().create_from_input(user)
        return Manager(user=user_db)


class EmployeeMapper(SimpleMapper[EmployeeSchema]):
    def __init__(self):
        super().__init__(EmployeeSchema)

    def create_from_input(self, user: CreateUserSchema):
        user_db = UserDBMapper().create_from_input(user)
        return Employee(grade_id=user.grade_id, office_id=user.office_id, user=user_db)
