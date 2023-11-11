import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { showMessage } from 'src/app/shared/common';
import { Role } from 'src/app/shared/models/user.model';
import { AuthService } from 'src/app/shared/services/auth.service';
import UserService from 'src/app/shared/services/user.service';
import { WebSocketService } from 'src/app/shared/services/websockets.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css', '../../../shared/shared.component.css'],
})
export class HeaderComponent implements OnInit {
  role!: Role;

  notifications: any[] = [];

  constructor(
    private authService: AuthService,
    private store: Store<any>,
    private router: Router,
    private userService: UserService,
    private wsService: WebSocketService,
    private snackbar: MatSnackBar,
  ) {
    this.store.subscribe((res) => {
      const role = res.user.profile.role.name;
      this.role = role;
    });
  }

  menuList = [
    {
      type: 'link',
      viewValue: 'Сотрудники',
      path: '/manager/employeers',
    },
    {
      type: 'link',
      viewValue: 'Пункты',
      path: '/manager/points',
    },
    {
      type: 'link',
      viewValue: 'Офисы',
      path: '/manager/offices',
      roles: ['Админ'],
    },
    {
      type: 'link',
      viewValue: 'Задачи',
      path: '/manager/task-page',
    },
    {
      type: 'devider',
    },
    {
      type: 'link',
      viewValue: 'Конструктор задач',
      path: '/manager/constructor',
    },
    {
      type: 'link',
      viewValue: 'Безопасность',
      path: '/manager/security-page',
    },
    {
      type: 'devider',
    },
    {
      type: 'action',
      viewValue: 'Выйти',
      action: () => this.logout(),
    },
  ];

  ngOnInit(): void {
    this.wsService.MessageGetted.subscribe((res: any) => {
      showMessage(this.snackbar, <string>res);
      this.notifications.push({
        id: -1,
        message: res,
      });
    });
    this.userService.getNotifications().subscribe((res: any) => {
      this.notifications = res.items;
    });
  }

  goToLink(link: string | undefined) {
    if (link) {
      this.router.navigate([link]);
    }
  }

  logout() {
    this.authService.DeleteTokens();
    this.router.navigate(['/auth/login']);
  }

  goToCabinet() {
    this.router.navigate(['/manager/profile']);
  }
}
