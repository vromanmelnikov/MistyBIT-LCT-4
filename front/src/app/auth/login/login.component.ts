import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { showMessage } from 'src/app/shared/common';
import { SigninModel } from 'src/app/shared/models/user.model';
import { AuthService } from 'src/app/shared/services/auth.service';
import ComponentsService from 'src/app/shared/services/components.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  // form = {
  //   email: '',
  //   password: ''
  // }

  form = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl(null, [
      Validators.required,
      Validators.minLength(8),
    ]),
  });

  constructor(
    private _snackBar: MatSnackBar,
    private authService: AuthService,
    private componentService: ComponentsService,
  ) {}

  ngOnInit(): void {
    this.authService.Authed.subscribe((res) => {
      showMessage(this._snackBar, res.msg.error.detail);
    });
  }

  sendRecover() {
    // this.componentService.openSnackbar('Письмо с ссылкой для восстановления пароля отправлено на почту')
    const { email } = this.form.value;
    this.authService.RecoverPassword(email).subscribe((res) => {
      this.componentService.openSnackbar(
        'Письмо с ссылкой для восстановления пароля отправлено на почту',
      );
    });
  }

  signin() {
    const { email, password } = this.form.value;

    // console.log({email, password})

    this.authService.Signin(new SigninModel(email, password));
  }
}
