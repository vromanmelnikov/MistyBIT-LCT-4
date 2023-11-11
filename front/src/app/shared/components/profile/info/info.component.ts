import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ChangeUserInfo, User } from 'src/app/shared/models/user.model';
import UserService from 'src/app/shared/services/user.service';
import { Store } from '@ngrx/store';
import { AuthService } from 'src/app/shared/services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.css'],
})
export class InfoComponent implements OnInit {
  user!: User;

  infoFormGroup = new FormGroup({
    lastname: new FormControl('', [Validators.required]),
    firstname: new FormControl('', [Validators.required]),
    patronymic: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required]),
  });

  constructor(
    private store: Store<any>,
    private userService: UserService,
    private authService: AuthService,
    private _snackBar: MatSnackBar,
  ) {}

  ngOnInit(): void {
    this.store.subscribe((res) => {
      const data = res.user.profile;
      this.user = data;
      this.setFormValues(data);
    });
  }

  setFormValues(data: any) {
    this.infoFormGroup.setValue({
      lastname: data.lastname,
      firstname: data.firstname,
      patronymic: data.patronymic,
      email: data.email,
    });
  }

  changeProfile() {
    const { lastname, firstname, patronymic } = this.infoFormGroup.value;
    this.userService
      //@ts-ignore
      .changeUserInfo(
        new ChangeUserInfo(
          lastname === null ? '' : <string>lastname,
          firstname === null ? '' : <string>firstname,
          patronymic === null ? '' : <string>patronymic,
        ),
      )
      .subscribe((res) => {
        this._snackBar.open('Данные профиля изменены', 'Хорошо', {
          horizontalPosition: 'center',
          verticalPosition: 'top',
        });
      });
  }

  changePassword() {
    this.authService.RecoverPassword(this.user.email).subscribe((res) => {
      this._snackBar.open(
        'Ссылка на восстановление отправлена на почту',
        'Хорошо',
        {
          horizontalPosition: 'center',
          verticalPosition: 'top',
        },
      );
    });
  }
}
