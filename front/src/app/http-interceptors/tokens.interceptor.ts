import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpInterceptor,
  HttpHandler,
  HttpRequest,
  HttpResponse,
  HttpErrorResponse,
  HttpClient,
} from '@angular/common/http';

import { Observable, ObservableInput, pipe, throwError } from 'rxjs';
import { catchError, map, retryWhen, switchMap } from 'rxjs/operators';
import { AuthService } from '../shared/services/auth.service';
import { TokensModel } from '../shared/models/tokens.model';
import { Router } from '@angular/router';
import { showMessage } from '../shared/common';
import { MatSnackBar } from '@angular/material/snack-bar';

/** Pass untouched request through to the next request handler. */
@Injectable()
export class TokensInterceptor implements HttpInterceptor {
  constructor(
    private authService: AuthService,
    private router: Router,
    private http: HttpClient,
    private _snackBar: MatSnackBar,
  ) {
    // console.log('туть')
  }

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler,
  ): Observable<HttpEvent<any>> {
    let token: string = '';

    if (req.url.includes('/auth/refresh_token')) {
      token = this.authService.GetRefreshToken();
    } else {
      token = this.authService.GetAccessToken();
    }

    if (token) {
      req = req.clone({
        headers: req.headers.set('Authorization', 'Bearer ' + token),
      });
    }

    return next.handle(req).pipe(
      catchError((error) => {
        if (error instanceof HttpErrorResponse) {

          const isNotInvalid = error.error.detail == 'Срок действия токена истек'

          const status = error.status;
          if (status === 401 && isNotInvalid) {
            this.authService
              .RefreshToken()
              .pipe(
                switchMap((res) => {
                  this.authService.SaveTokens(<any>res);
                  token = this.authService.GetAccessToken();
                  req = req.clone({
                    headers: req.headers.set(
                      'Authorization',
                      'Bearer ' + token,
                    ),
                  });
                  const url = window.location.pathname;
                  this.router.navigate([url]);
                  return next.handle(req);
                }),
              )
              .subscribe(
                (res) => {},
                (error) => {
                  this.authService.DeleteTokens();
                  this.router.navigate(['/auth/login']);
                },
              );
          }
          else if (status === 401 && isNotInvalid === false) {
            // showMessage(this._snackBar, 'Неправильные данные!');
          } 
          else if (status === 403 ) {
            showMessage(this._snackBar, 'Метод вам не доступен!');
          } else if (status === 404) {
            return throwError({ items: [] });
          }
        }
        return throwError(error);
      }),
    );
  }
}
