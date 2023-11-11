export interface Skill {
  id: number;
  name: string;
}

export interface Office {
  id: number;
  address: string;
}

export interface Grade {
  id: number;
  name: string;
}

export class EmployeeInfo {
  constructor(
    public office: Office,
    public skill_links: any,
    public grade: any,
  ) {}
}

interface WorkerParams {
  id: number;
  lastname: string;
  firstname: string;
  patronymic: string;
  email: string;
}

interface EmployeerParams extends WorkerParams {
  grade: Grade;
  office: Office;
  skills?: Skill[];
}

interface ManagerParams extends WorkerParams {}

class Worker {
  id = -1;
  lastname = '';
  firstname = '';
  patronymic = '';
  email = '';

  constructor(params: WorkerParams) {
    this.id = params.id;
    this.lastname = params.lastname;
    this.firstname = params.firstname;
    this.patronymic = params.patronymic;
    this.email = params.email;
  }
}

export class Employeer extends Worker {
  office: Office = {
    id: -1,
    address: '',
  };
  grade: Grade = {
    id: -1,
    name: '',
  };

  skills?: Skill[] = [];

  constructor(params: EmployeerParams) {
    super(params);
    this.office = params.office;
    this.grade = params.grade;
    if (params.skills) {
      this.skills = params.skills;
    }
  }
}

export class Manager extends Worker {
  constructor(params: ManagerParams) {
    super(params);
  }
}

export class Employee {
  constructor(
    public id: number,
    public email: string,
    public lastname: string,
    public firstname: string,
    public patronymic: string,
    public is_active: boolean,
    public grade_name: string,
    public grade_id: number,
    public office_address: string,
    public office_id: number,
    public img: string,
  ) {}
}
