import { Component, OnInit } from '@angular/core';
import UserService from '../shared/services/user.service';
import { User } from '../shared/models/user.model';
import { EmployeeInfo } from '../shared/models/employers.model';
import EmployeeService from '../shared/services/employee.service';

import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import {
  SetStaticUserInfo,
  setUser,
  setUserSkills,
} from '../store/user.actions';
import { AuthService } from '../shared/services/auth.service';
import { ActivatedRoute, Router } from '@angular/router';
import SecurityService from '../shared/services/security.service';
import { WebSocketService } from '../shared/services/websockets.service';

@Component({
  selector: 'app-system',
  templateUrl: './system.component.html',
  styleUrls: ['./system.component.css', '../shared/shared.component.css'],
})
export class SystemComponent implements OnInit {
  profile!: Observable<User>;

  constructor(
    private store: Store<any>,
    private userService: UserService,
    private activateRoute: ActivatedRoute,
    private wsService: WebSocketService
  ) {

    this.activateRoute.data.subscribe((res: any) => {

      const user = res.profile as User;
      this.userService.userInfo = user;

      this.store.dispatch(setUser(user));

      const employeeInfo = res.profile.employee as EmployeeInfo;

      if (employeeInfo) {
        this.store.dispatch(setUserSkills(employeeInfo.skill_links));
        this.store.dispatch(
          SetStaticUserInfo(employeeInfo.office, employeeInfo.grade),
        );
      }

      wsService.Connect()

    });
  }

  ngOnInit(): void {}
}
