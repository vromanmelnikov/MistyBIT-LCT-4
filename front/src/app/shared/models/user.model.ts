export class SigninModel {
  constructor(
    public username: any,
    public password: any,
  ) {}
}

export class Role {
  constructor(
    public id: number,
    public name: string,
    public is_public: boolean,
  ) {}
}

export class Office {
  constructor(
    public id: number,
    public address: string,
  ) {}
}

export class Grade {
  constructor(
    public id: number,
    public name: string,
  ) {}
}

export class ChangeUserInfo {
  constructor(
    public lastname: string | null,
    public firstname: string | null,
    public patronymic: string | null,
    public id?: number,
  ){}
}

export class User {
  constructor(
    public email: string,
    public lastname: string,
    public firstname: string,
    public patronymic: string,
    public id: number,
    public img: string,
    public role: Role,
  ) {}
}

export class EmployeeInfo {
  constructor(
    public office: Office,
    public skills: any,
    public grade: any,
  ) {}
}

export class SignupModel {
  constructor() {}
}
export class SignupHiddenModel {
  constructor() {}
}

export class UpdateUserModel {
  constructor() {}
}

export class FullUser {
  constructor() {}
}
