import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Employee } from 'src/app/shared/models/employers.model';
import { Grade, Office, Role } from 'src/app/shared/models/user.model';
import StaticService from 'src/app/shared/services/static.service';
import UserService, { AddUserParams } from 'src/app/shared/services/user.service';

interface addEmployeeDialogData {
  allGrades: Grade[];
  allOffices: Office[];
  allRoles: Role[];
}

@Component({
  selector: 'app-add-employye-dialog',
  templateUrl: './add-employye-dialog.component.html',
  styleUrls: ['./add-employye-dialog.component.css'],
})
export class AddEmployyeDialogComponent implements OnInit {
  allGrades: Grade[] = this.data.allGrades;
  allOffices: Office[] = this.data.allOffices;
  allRoles: Role[] = this.data.allRoles;

  selectedRole: string | null = null;

  form = new FormGroup({
    email: new FormControl('', []),
    lastname: new FormControl('', []),
    firstname: new FormControl('', []),
    patronymic: new FormControl('', []),
    grade: new FormControl('', []),
    office: new FormControl('', []),
  });

  constructor(
    public dialogRef: MatDialogRef<AddEmployyeDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: addEmployeeDialogData,
    private userService: UserService,
    private staticService: StaticService,
  ) {}

  onNoClick(): void {
    const { lastname, firstname, patronymic, grade, office } = this.form.value;

    //@ts-ignore
    let infoResult = this.changeInfo(lastname, firstname, patronymic);
  }

  ngOnInit(): void {
    this.allRoles = this.allRoles.filter((item) => item.name !== 'Админ');
  }

  registation() {
    const { email, lastname, firstname, patronymic, office, grade } =
      this.form.value;

    const role_id = this.allRoles.filter(item => item.name == this.selectedRole)[0].id

    //@ts-ignore
    let data: AddUserParams = { email, lastname, firstname, patronymic, role_id };

    let office_id = null;
    let grade_id = null;

    if (this.selectedRole == 'Сотрудник') {
      office_id = this.allOffices.filter((item) => item.address === office)[0].id;
      grade_id = this.allGrades.filter((item) => item.name === grade)[0].id;
      data.office_id = office_id
      data.grade_id = grade_id
    }

    this.userService.addUser(data).subscribe(
      res => {
        console.log(res)
      }
    );
  }
}
