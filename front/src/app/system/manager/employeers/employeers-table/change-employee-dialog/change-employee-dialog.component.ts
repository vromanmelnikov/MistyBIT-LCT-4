import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Employee } from 'src/app/shared/models/employers.model';
import { Grade, Office } from 'src/app/shared/models/user.model';
import StaticService from 'src/app/shared/services/static.service';
import UserService from 'src/app/shared/services/user.service';

export interface ChangeEmployeeDialogData {
  employee: Employee;
  allGrades: Grade[];
  allOffices: Office[]
}

@Component({
  selector: 'app-change-employee-dialog',
  templateUrl: './change-employee-dialog.component.html',
  styleUrls: ['./change-employee-dialog.component.css'],
})
export class ChangeEmployeeDialogComponent implements OnInit {

  allGrades: Grade[] = this.data.allGrades;
  allOffices: Office[] = this.data.allOffices;

  checked: boolean = false

  form = new FormGroup({
    email: new FormControl(this.data.employee.email, []),
    lastname: new FormControl(this.data.employee.lastname, []),
    firstname: new FormControl(this.data.employee.firstname, []),
    patronymic: new FormControl(this.data.employee.patronymic, []),
    grade: new FormControl(this.data.employee.grade_name, []),
    office: new FormControl(this.data.employee.office_address, []),
  });

  constructor(
    public dialogRef: MatDialogRef<ChangeEmployeeDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ChangeEmployeeDialogData,
    private userService: UserService,
    private staticService: StaticService,
  ) {}

  onNoClick(): void {
    const { lastname, firstname, patronymic, grade, office } = this.form.value;

    //@ts-ignore  
    let infoResult = this.changeInfo(lastname, firstname, patronymic)

    if (infoResult) {
      infoResult.subscribe(
        res => {
          console.log(res)
        }
      )
    }

    let employeeInfoResult = this.changeGradeAndOffice(<string>grade, <string>office)

    if (employeeInfoResult) {
      employeeInfoResult.subscribe(
        res => {
          console.log(res)
        }
      )
    }

    // this.dialogRef.close();
  }

  ngOnInit(): void {
    this.checked = this.data.employee.is_active
  }

  changeGradeAndOffice(grade_name: string, office_address: string) {

    if (this.data.employee.grade_name != grade_name || this.data.employee.office_address != office_address) {

      const newGradeID = this.allGrades.filter(item => item.name === grade_name)[0]
      const newOfficeID = this.allOffices.filter(item => item.address === office_address)[0]
      
      return this.userService.changeEmployeeInfo(this.data.employee.id, newGradeID.id, newOfficeID.id)

    }
    else {
      return null
    }
  }

  changeInfo(lastname: string, firstname: string, patronymic: string) {

    if (
      lastname != this.data.employee.lastname ||
      firstname != this.data.employee.firstname ||
      patronymic != this.data.employee.firstname
    ) {
      return this.userService.changeUserInfo({id: this.data.employee.id, lastname, firstname, patronymic})
    }
    else {
      return null
    }
  }

  changeStatus() {
    this.userService.changeStatus(this.data.employee.id).subscribe(
      res => {
        
      }
    )
  }
}
