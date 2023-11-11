import { EventEmitter, Injectable, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import StaticService from './static.service';
import { Role } from '../models/user.model';

@Injectable()
export default class EmployeeService {
  USERS_URL = `${environment.API_URL}/users`;

  constructor(private http: HttpClient, private staticService: StaticService) {}

  getAllEmployees(office_id?: number, limit?: number, offset?: number) {
    let params: any = {};

    if (office_id) {
      params.office_id = office_id;
    }
    if (limit) {
      params.limit = limit;
    }
    if (offset) {
      params.offset = offset;
    }

    return this.http.get(`${this.USERS_URL}/employees/all`, {
      params: { ...params },
    });
  }

  async getAllmanagers() {

    const managerRoleID: number = await new Promise(
      (resolve, reject) => {
        this.staticService.getAllRoles().subscribe(
          res => {
            if (res.items) {
              const managerRoleID = res.items.filter((item: Role) => item.name === 'Менеджер')[0].id
              resolve(managerRoleID)
            }
            reject(null)
          }
        )
      }
    )

    return this.http.get(`${this.USERS_URL}/all`, {
      params: { role_id: managerRoleID },
    }); 

  }

}
