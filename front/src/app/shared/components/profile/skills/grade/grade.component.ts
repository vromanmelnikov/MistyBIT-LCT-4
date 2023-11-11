import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { Grade } from 'src/app/shared/models/employers.model';
import { Role } from 'src/app/shared/models/user.model';
import EmployeeService from 'src/app/shared/services/employee.service';

@Component({
  selector: 'app-grade',
  templateUrl: './grade.component.html',
  styleUrls: ['./grade.component.css'],
})
export class GradeComponent implements OnInit {

  grade: Grade = {
    id: -1,
    name: '',
  };

  role: Role = {
    id: -1,
    name: 'Сотрудник',
    is_public: true
  }

  constructor(private store: Store<any>, private employeeService: EmployeeService) {}

  ngOnInit(): void {

    this.store.subscribe(
      res => {
        this.grade = res.user.grade
        this.role = res.user.profile.role
      }
    )

  }
}
