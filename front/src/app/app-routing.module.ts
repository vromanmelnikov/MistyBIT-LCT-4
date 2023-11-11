import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NotFoundPageComponent } from './not-found-page/not-found-page.component';
import { AppComponent } from './app.component';
import { ProfileResolver } from './shared/guards/profile.resolver';
import { BackIsFallComponent } from './back-is-fall/back-is-fall.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'employee/profile',
    pathMatch: 'full',
  },
  {
    path: '',
    loadChildren: () =>
      import('./system/system.module').then((m) => m.SystemModule),
    resolve: {
      profile: ProfileResolver,
    },
  },
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.module').then((m) => m.AuthModule),
  },
  { path: 'not_found', pathMatch: 'full', component: NotFoundPageComponent },
  { path: '**', pathMatch: 'full', component: NotFoundPageComponent },
  { path: 'back_is_fall', component: BackIsFallComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
