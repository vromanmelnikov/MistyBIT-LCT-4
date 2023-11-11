import { HttpClient } from '@angular/common/http';
import { Injectable, Output, EventEmitter } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { environment } from 'src/environments/environment';
import { HttpErrorResponse } from '@angular/common/http';

@Injectable()
export default class SecurityService {
  SECURITY_URL = `${environment.API_URL}/secure`;
  constructor(private http: HttpClient) {}

  getSecurityMethods() {
    return this.http.get(`${this.SECURITY_URL}/methods/all`).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  getPolicyMethod(action: string, resource: string) {
    let params: any = {};
    if (action) {
      params.action = action;
    }
    if (resource) {
      params.resource = resource;
    }
    return this.http
      .get(`${this.SECURITY_URL}/policies/all`, {
        params: { ...params },
      })
      .pipe(
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }),
      );
  }

  updatePolicy(policy: any) {
    return this.http.put(`${this.SECURITY_URL}/policies`, policy).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
}
