import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  CanActivate,
  CanActivateChild,
  Router,
  RouterStateSnapshot,
} from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Store, select } from '@ngrx/store';
import { map, tap } from 'rxjs';

@Injectable()
export class EmployeeGuard implements CanActivate, CanActivateChild {
  constructor(
    private store: Store<any>,
    private authService: AuthService,
    private router: Router,
  ) {}

  async canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ): Promise<any> {
    this.store.subscribe((res) => {
      const role = res.user.profile.role;
      if (role.id !== -1 && role.name !== 'Сотрудник') {
        console.log(role)
        this.router.navigate(['/manager/profile']);
      }
    });
  }

  canActivateChild(
    childRoute: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ): any {
    return this.canActivate(childRoute, state);
  }
}
