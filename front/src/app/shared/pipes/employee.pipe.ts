import { Pipe, PipeTransform } from '@angular/core';
import { Employee } from '../models/employers.model';

@Pipe({
  name: 'employee',
})
export class EmployeePipe implements PipeTransform {
  transform(employees: any, ...args: any[]) {
    let res = employees.map((value: any): Employee => {
      const item: Employee = {
        id: value.user.id,
        email: value.user.email,
        lastname: value.user.lastname,
        firstname: value.user.firstname,
        patronymic: value.user.patronymic,
        is_active: value.user.is_active,
        grade_name: value.grade.name,
        grade_id: value.grade.id,
        office_address: value.office.address,
        office_id: value.office.id,
        img: value.user.img,
      };
      return item;
    });
    return res;
  }
}
