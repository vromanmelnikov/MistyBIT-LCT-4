import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  Resolve,
  Router,
  RouterStateSnapshot,
} from '@angular/router';
import UserService from '../services/user.service';
import { Observable, catchError, throwError } from 'rxjs';
import { User } from '../models/user.model';
import { AuthService } from '../services/auth.service';

@Injectable({ providedIn: 'root' })
export class ProfileResolver implements Resolve<any> {
  constructor(private userService: UserService, private router: Router, private authService: AuthService) {}

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): any {
    return this.userService.getUserProfile().pipe(
      catchError(
        (error) => {
          const flag = this.authService.IsLoggedIn()
          if (flag === false) {
            this.router.navigate(['/auth/login'])
          }
          if (error.status === 0) {
            this.router.navigate(['/back_is_fall'])
          }
          return throwError(error)
        }
      )
    );
  }
}
