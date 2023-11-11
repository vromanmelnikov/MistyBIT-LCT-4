import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Employee, Manager } from 'src/app/shared/models/employers.model';
import { Grade, Office } from 'src/app/shared/models/user.model';
import StaticService from 'src/app/shared/services/static.service';
import UserService from 'src/app/shared/services/user.service';

export interface ChangeManagerDialogData {
  manager: Manager;
}

@Component({
  selector: 'app-change-manager-dialog',
  templateUrl: './change-manager-dialog.component.html',
  styleUrls: ['./change-manager-dialog.component.css']
})
export class ChangeManagerDialogComponent implements OnInit {

  form = new FormGroup({
    email: new FormControl(this.data.manager.email, []),
    lastname: new FormControl(this.data.manager.lastname, []),
    firstname: new FormControl(this.data.manager.firstname, []),
    patronymic: new FormControl(this.data.manager.patronymic, []),
  });

  constructor(
    public dialogRef: MatDialogRef<ChangeManagerDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ChangeManagerDialogData,
    private userService: UserService,
    private staticService: StaticService,
  ) {}

  onNoClick(): void {
    const { lastname, firstname, patronymic } = this.form.value;

    //@ts-ignore  
    let infoResult = this.changeInfo(lastname, firstname, patronymic)

    if (infoResult) {
      infoResult.subscribe(
        res => {
          console.log(res)
        }
      )
    }

    // this.dialogRef.close();
  }

  ngOnInit(): void {
    
  }

  changeInfo(lastname: string, firstname: string, patronymic: string) {

    if (
      lastname != this.data.manager.lastname ||
      firstname != this.data.manager.firstname ||
      patronymic != this.data.manager.firstname
    ) {
      return this.userService.changeUserInfo({id: this.data.manager.id, lastname, firstname, patronymic})
    }
    else {
      return null
    }
  }

}
