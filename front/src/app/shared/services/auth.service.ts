import { HttpClient } from '@angular/common/http';
import { EventEmitter, Injectable, Output } from '@angular/core';
import {
  SigninModel,
  SignupHiddenModel,
  SignupModel,
  User,
} from '../models/user.model';
import { CookieService } from './cookie.service';
import { TokensModel } from '../models/tokens.model';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import UserService from './user.service';

const KEY_ACCESS_TOKEN = 'access_token';
const KEY_REFRESH_TOKEN = 'refresh_token';
const EXPIRES_ACCESS_TOKEN = 1;
const EXPIRES_REFRESH_TOKEN = 7;

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private httpClient: HttpClient,
    private cookieService: CookieService,
    private router: Router,
    private userService: UserService,
  ) {}
  @Output() Authed = new EventEmitter<any>();
  @Output() TokenRefreshed = new EventEmitter();

  Signin(signinModel: SigninModel) {
    // console.log(signinModel);

    const formData = new FormData();

    formData.set('username', signinModel.username);
    formData.set('password', signinModel.password);

    return this.httpClient
      .post(`${environment.API_URL}/auth/signin`, formData)
      .subscribe(
        (res: any) => {
          this.SaveTokens(res as TokensModel);
          this.Authed.emit({ res: true });
          this.userService.getUserProfile().subscribe(
            (res: any) => {
              const role = res.role.name
              if (role == 'Админ' || role == 'Менеджер') {
                this.router.navigate(['/manager/profile']);
              }
              else {
                this.router.navigate(['/employee/profile']);
              }
            }
          )
        },
        (err: any) => {
          console.log(err);
          this.Authed.emit({ res: false, msg: err });
        },
      );
  }

  IsLoggedIn() {
    return this.cookieService.GetCookie(KEY_REFRESH_TOKEN) != null;
  }

  RecoverPassword(email: any) {
    console.log(email)
    return this.httpClient.post(
      `${environment.API_URL}/auth/password/recover`,
      {
        email,
      },
    );
  }

  ResetPassword(code: string, password: string) {
    return this.httpClient.post(`${environment.API_URL}/auth/password/reset`, {
      code,
      password,
    });
  }

  Signup(signupModel: SignupModel) {
    this.httpClient
      .post(`${environment.API_URL}/signup_to_intern`, signupModel)
      .subscribe(
        (res: any) => {
          this.SaveTokens(res as TokensModel);
          this.Authed.emit({ res: true });
        },
        (err: any) => {
          this.Authed.emit({ res: false, msg: err });
        },
      );
  }

  SignupHidden(signupModel: SignupHiddenModel) {
    this.httpClient
      .post(`${environment.API_URL}/signup_to_not_intern`, signupModel)
      .subscribe(
        (res: any) => {
          this.SaveTokens(res as TokensModel);
          this.Authed.emit({ res: true });
        },
        (err: any) => {
          this.Authed.emit({ res: false, msg: err });
        },
      );
  }

  RefreshToken() {
    let refresh_token = this.cookieService.GetCookie(KEY_REFRESH_TOKEN);
    let access_token = this.cookieService.GetCookie(KEY_ACCESS_TOKEN);
    console.log({ access_token, refresh_token });
    return this.httpClient.post(`${environment.API_URL}/auth/refresh_token`, {
      headers: { Authorization: `Bearer ${refresh_token}` },
    });
  }

  DeleteTokens() {
    this.cookieService.DeleteCookie(KEY_ACCESS_TOKEN);
    this.cookieService.DeleteCookie(KEY_REFRESH_TOKEN);
  }

  SaveTokens(pair: TokensModel) {
    this.cookieService.SetCookie({
      name: KEY_ACCESS_TOKEN,
      value: pair.access_token,
      expireDays: EXPIRES_ACCESS_TOKEN,
      secure: true,
    });
    this.cookieService.SetCookie({
      name: KEY_REFRESH_TOKEN,
      value: pair.refresh_token,
      expireDays: EXPIRES_REFRESH_TOKEN,
      secure: true,
    });
  }

  GetAccessToken() {
    let token = this.cookieService.GetCookie(KEY_ACCESS_TOKEN);
    return token != null ? token : '';
  }

  GetRefreshToken() {
    let token = this.cookieService.GetCookie(KEY_REFRESH_TOKEN);
    return token != null ? token : '';
  }
}
