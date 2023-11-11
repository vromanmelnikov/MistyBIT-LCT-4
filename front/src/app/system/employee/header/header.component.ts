import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { showMessage } from 'src/app/shared/common';
import { AuthService } from 'src/app/shared/services/auth.service';
import UserService from 'src/app/shared/services/user.service';
import { WebSocketService } from 'src/app/shared/services/websockets.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css', '../../../shared/shared.component.css'],
})
export class HeaderComponent implements OnInit {

  notifications: any[] = [];
  
  constructor(
    private authService: AuthService,
    private router: Router,
    private userService: UserService,
    private wsService: WebSocketService,
    private snackbar: MatSnackBar,
  ) {}

  menuList = [
    {
      type: 'link',
      viewValue: 'Задачи',
      path: '/employee/tasks',
    },
    {
      type: 'devider'
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

  goToCabinet() {
    this.router.navigate(['/employee/profile']);
  }

  logout() {
    this.authService.DeleteTokens()
    this.router.navigate(['/auth/login']);
  }
}
