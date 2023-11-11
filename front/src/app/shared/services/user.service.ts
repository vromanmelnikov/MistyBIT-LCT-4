import { EventEmitter, Injectable, Output } from '@angular/core';
import { EmployeeInfo } from '../models/employers.model';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { ChangeUserInfo, User } from '../models/user.model';
import { catchError, throwError } from 'rxjs';

export interface AddUserParams {
  email: string;
  lastname: string;
  firstname: string;
  patronymic: string;
  role_id: number;
  grade_id?: number;
  office_id?: number;
}

@Injectable()
export default class UserService {
  USERS_URL = `${environment.API_URL}/users`;

  constructor(private http: HttpClient) {}

  public userInfo: User = {
    lastname: 'Иванов',
    firstname: 'Иван',
    patronymic: 'Иванович',
    email: 'ivanov@mail.ru',
    id: -1,
    img: '',
    role: {
      id: -1,
      name: 'Админ',
      is_public: false,
    },
  };

  @Output() ProfileLoaded = new EventEmitter<any>();

  addUser(data: AddUserParams) {
    return this.http.post(this.USERS_URL + '/registration', data);
  }

  getUserProfile(id?: number) {
    return this.http.get(this.USERS_URL + '/profile');
  }

  getAllSkills() {
    return this.http.get(this.USERS_URL + '/skills/all').pipe(
      //@ts-ignore
      catchError((error: any) => {
        if (error.status === 404) return throwError([]);
      }),
    );
  }

  changeUserInfo(data: ChangeUserInfo) {

    let params: any = {}

    if (data.id) {
      params.id = data.id
    }

    return this.http.put(
      this.USERS_URL,
      {
        lastname: data.lastname,
        firstname: data.firstname,
        patronymic: data.patronymic,
      },
      {
        params,
      },
    );
  }

  changeUserImage(data: FormData) {
    console.log(data);
    return this.http.post(this.USERS_URL + '/image', data);
  }

  deleteUserImage() {
    return 
  }

  changeEmployeeInfo(id: number, grade_id: number, office_id: number) {
    return this.http.put(this.USERS_URL + '/employees', {
      id,
      grade_id,
      office_id,
    });
  }

  addSkill(id: number) {
    return this.http.post(this.USERS_URL + '/skills/employee', {
      skill_id: id,
    });
  }

  addNewSkill(name: string) {
    return this.http.post(this.USERS_URL + '/skills', {
      name,
    });
  }

  deleteSkill(id: number) {
    return this.http.delete(this.USERS_URL + `/skills/employee?id=${id}`);
  }

  changeStatus(id: number) {
    return this.http.put(this.USERS_URL + `/is_active`, {}, {params: {user_id: id}})
  }

  getNotifications() {
    return this.http.get(`${environment.API_URL}/notifications/`);
  }

}
