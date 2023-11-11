import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { EmployeeRoutingModule } from './employee-routing.module';
import { EmployeeComponent } from './employee.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { HeaderComponent } from './header/header.component';
import { TasksComponent } from './tasks/tasks.component';
import { CurrentTaskComponent } from './current-task/current-task.component';
import { ListComponent } from './tasks/list/list.component';
import { MapComponent } from './tasks/map/map.component';
import TasksService from 'src/app/shared/services/tasks.service';
import { RemainTaskComponent } from './tasks/list/remain-task/remain-task.component';
import { CompletedTaskComponent } from './tasks/list/completed-task/completed-task.component';
import EmployeeService from 'src/app/shared/services/employee.service';
import { FormFieldComponent } from 'src/app/shared/components/form-field/form-field.component';
import { FeedbackDialogComponent } from './feedback-dialog/feedback-dialog.component';
import { ErorrDialogComponent } from './error-dialog/error-dialog.component';
import { ArchieveListTaskComponent } from './tasks/list/archieve-list-task/archieve-list-task.component';


@NgModule({
  declarations: [
    EmployeeComponent,
    HeaderComponent,
    TasksComponent,
    CurrentTaskComponent,
    ListComponent,
    MapComponent,
    RemainTaskComponent,
    CompletedTaskComponent,
    FeedbackDialogComponent,
    ErorrDialogComponent,
    ArchieveListTaskComponent,
  ],
  imports: [
    CommonModule,
    EmployeeRoutingModule,
    SharedModule
  ],
  providers: [
  ]
})
export class EmployeeModule { }
