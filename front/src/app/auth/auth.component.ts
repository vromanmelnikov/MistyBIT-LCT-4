import { Component, OnInit } from '@angular/core';
import { ActivationEnd, NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css'],
})
export class AuthComponent implements OnInit {
  title: string = 'Авторизация';

  constructor(private router: Router) {
    router.events.subscribe((route) => {
      if (route instanceof NavigationEnd) {
        console.log(route);

        if (route.url === '/auth/login') {
          this.title = 'Авторизация';
        } else if (route.url === '/auth/registration') {
          this.title = 'Регистрация';
        } else if (route.url === '/auth/reset') {
          this.title = 'Смена пароля';
        } else if (route.url === '/auth/recovery') {
          this.title = 'Восстановление пароля';
        }
      }
    });
  }

  ngOnInit(): void {}
}
