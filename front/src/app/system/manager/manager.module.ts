import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ManagerRoutingModule } from './manager-routing.module';
import { ManagerComponent } from './manager.component';
import { TasksComponent } from './tasks/tasks.component';
import { PointsComponent } from './points/points.component';
import { HeaderComponent } from './header/header.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { EmployeersComponent } from './employeers/employeers.component';
import { EmployeersTableComponent } from './employeers/employeers-table/employeers-table.component';
import { ManagersTableComponent } from './employeers/managers-table/managers-table.component';
import EmployeersManagmentService from 'src/app/shared/services/employeers-managment.service';
import { PointsTableComponent } from './points/points-table/points-table.component';
import { ArchiveComponent } from './employeers/archive/archive.component';
import { DateItemComponent } from './employeers/archive/date-item/date-item.component';
import { ItemComponent } from './employeers/archive/date-item/item/item.component';
import { TaskConstructorComponent } from './task-constructor/task-constructor.component';
import { WorkerTableComponent } from './employeers/worker-table/worker-table.component';
import { ChangeEmployeeDialogComponent } from './employeers/employeers-table/change-employee-dialog/change-employee-dialog.component';
import { ChangePointDialogComponent } from './points/points-table/change-point-dialog/change-point-dialog.component';
import { AddPointDialogComponent } from './points/points-table/add-point-dialog/add-point-dialog.component';
import { AddEmployyeDialogComponent } from './employeers/add-employye-dialog/add-employye-dialog.component';
import { ChangeManagerDialogComponent } from './employeers/managers-table/change-manager-dialog/change-manager-dialog.component';
import { OfficesComponent } from './offices/offices.component';
import { OfficeComponent } from './offices/office/office.component';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { TaskListComponent } from './task-constructor/task-list/task-list.component';
import { TaskComponent } from './task-constructor/task-list/task/task.component';
import { AddOfficeDialogComponent } from './offices/add-office-dialog/add-office-dialog.component';
import { CreateTaskComponent } from './task-constructor/create-task/create-task.component';
import { ConditionComponent } from './task-constructor/create-task/condition/condition.component';
import { SubconditionComponent } from './task-constructor/create-task/condition/subcondition/subcondition.component';
import { TaskPageComponent } from './task-page/task-page.component';
import { SecurityComponent } from './security/security.component';
import { SkillsComponent } from './task-constructor/task-list/task/skills/skills.component';
import { SkillsListComponent } from './task-constructor/skills-list/skills-list.component';
import { ChangeOfficeDialogComponent } from './offices/office/change-office-dialog/change-office-dialog.component';

@NgModule({
  declarations: [
    ManagerComponent,
    TasksComponent,
    PointsComponent,
    HeaderComponent,
    EmployeersComponent,
    EmployeersTableComponent,
    ManagersTableComponent,
    HeaderComponent,
    PointsTableComponent,
    ArchiveComponent,
    DateItemComponent,
    ItemComponent,
    TaskConstructorComponent,
    WorkerTableComponent,
    ChangeEmployeeDialogComponent,
    ChangePointDialogComponent,
    AddPointDialogComponent,
    AddEmployyeDialogComponent,
    ChangeManagerDialogComponent,
    OfficesComponent,
    OfficeComponent,
    TaskListComponent,
    TaskComponent,
    AddOfficeDialogComponent,
    CreateTaskComponent,
    ConditionComponent,
    SubconditionComponent,
    TaskPageComponent,
    SecurityComponent,
    SkillsComponent,
    SkillsListComponent,
    ChangeOfficeDialogComponent,
  ],
  imports: [
    CommonModule,
    ManagerRoutingModule,
    SharedModule,
    MatSnackBarModule,
  ],
  providers: [
    EmployeersManagmentService
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ManagerModule {}
