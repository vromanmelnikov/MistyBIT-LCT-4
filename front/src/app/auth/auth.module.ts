import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AuthRoutingModule } from './auth-routing.module';
import { AuthComponent } from './auth.component';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';
import { SharedModule } from '../shared/shared.module';
import { ResetComponent } from './reset/reset.component';
import ComponentsService from '../shared/services/components.service';

@NgModule({
  declarations: [
    AuthComponent,
    LoginComponent,
    RegistrationComponent,
    ResetComponent,
  ],
  imports: [CommonModule, AuthRoutingModule, SharedModule],
  providers: [
    ComponentsService,
    // UserService,
    // AuthService
  ],
})
export class AuthModule {}
