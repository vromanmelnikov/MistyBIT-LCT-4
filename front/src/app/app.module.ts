import { SecurityComponent } from './system/manager/security/security.component';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NotFoundPageComponent } from './not-found-page/not-found-page.component';
import { SharedModule } from './shared/shared.module';
import RoutesService from './shared/services/routes.service';
import { environment } from 'src/environments/environment';
import { AngularYandexMapsModule, YaConfig } from 'angular8-yandex-maps';
import { AuthService } from './shared/services/auth.service';
import { httpInterceptorProviders } from './http-interceptors';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { TokensInterceptor } from './http-interceptors/tokens.interceptor';
import UserService from './shared/services/user.service';
import EmployeeService from './shared/services/employee.service';
import TasksService from './shared/services/tasks.service';
import RootStoreModule from './store';
import { AuthGuard } from './shared/guards/auth.guard';
import { EmployeeGuard } from './shared/guards/employeer.guard';
import StaticService from './shared/services/static.service';
import ComponentsService from './shared/services/components.service';
import TaskService from './shared/services/task.service';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import SecurityService from './shared/services/security.service';
import { BackIsFallComponent } from './back-is-fall/back-is-fall.component';
import { WebSocketService } from './shared/services/websockets.service';

const mapConfig: YaConfig = {
  apikey: environment.API_KEY,
  lang: 'ru_RU',
};

@NgModule({
  declarations: [AppComponent, NotFoundPageComponent, BackIsFallComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    AngularYandexMapsModule.forRoot(mapConfig),
    HttpClientModule ,
    RootStoreModule,
    MatSnackBarModule
  ],
  providers: [
    RoutesService,
    AuthService,
    UserService,
    EmployeeService,
    TasksService,
    TaskService,
    httpInterceptorProviders,
    AuthGuard,
    EmployeeGuard,
    StaticService,
    ComponentsService,
    SecurityService,
    WebSocketService
    // MatSnackBar
    // { provide: HTTP_INTERCEPTORS, useClass: TokensInterceptor, multi: true},
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
