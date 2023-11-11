import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ManagerComponent } from './manager.component';
import { EmployeersComponent } from './employeers/employeers.component';
import { PointsComponent } from './points/points.component';
import { TaskConstructorComponent } from './task-constructor/task-constructor.component';
import { ProfileComponent } from 'src/app/shared/components/profile/profile.component';
import { OfficesComponent } from './offices/offices.component';
import { TaskPageComponent } from './task-page/task-page.component';
import { SecurityComponent } from './security/security.component';

const routes: Routes = [
  {
    path: '',
    component: ManagerComponent,
    children: [
      {
        path: 'employeers',
        component: EmployeersComponent,
      },
      {
        path: 'points',
        component: PointsComponent,
      },
      {
        path: 'constructor',
        component: TaskConstructorComponent,
      },
      {
        path: 'profile',
        component: ProfileComponent,
      },
      {
        path: 'offices',
        component: OfficesComponent,
      },
      {
        path: 'task-page',
        component: TaskPageComponent,
      },
      {
        path: 'security-page',
        component: SecurityComponent,
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ManagerRoutingModule {}
