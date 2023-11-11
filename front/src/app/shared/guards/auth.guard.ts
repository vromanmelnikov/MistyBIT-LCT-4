import {
  ActivatedRouteSnapshot,
  CanActivate,
  CanActivateChild,
  Router,
  RouterStateSnapshot,
  UrlTree,
} from '@angular/router';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Store } from '@ngrx/store';

@Injectable()
export class AuthGuard implements CanActivate, CanActivateChild {
  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): any {

    console.log('Проверка авторизации...')

    if (this.authService.IsLoggedIn()) {
      return true;
    } else {
      // this.router.navigate(['/auth/login']);
    }
  }

  canActivateChild(
    childRoute: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ): any {
    return this.canActivate(childRoute, state);
  }
}

// boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree>
