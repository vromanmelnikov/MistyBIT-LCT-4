import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SystemComponent } from './system.component';
import { AuthGuard } from '../shared/guards/auth.guard';
import { EmployeeGuard } from '../shared/guards/employeer.guard';

const routes: Routes = [
  {
    path: '',
    component: SystemComponent,
    canActivate: [AuthGuard],
    // canActivate: [],
    children: [
      {
        path: 'manager',
        loadChildren: () => import('./manager/manager.module').then((module) => module.ManagerModule)
      },
      {
        path: 'employee',
        loadChildren: () => import('./employee/employee.module').then((module) => module.EmployeeModule),
        canActivate: [EmployeeGuard]
      },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SystemRoutingModule { }
