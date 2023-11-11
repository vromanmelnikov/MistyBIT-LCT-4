import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EmployeeComponent } from './employee.component';
import { TasksComponent } from './tasks/tasks.component';
import { ProfileComponent } from 'src/app/shared/components/profile/profile.component';

const routes: Routes = [
	{
		path: '',
		component: EmployeeComponent,
		children: [
			{
				path: 'profile',
				component: ProfileComponent
			},
			{
				path: 'tasks',
				component: TasksComponent
			},
		]
	}
];

@NgModule({
	imports: [RouterModule.forChild(routes)],
	exports: [RouterModule]
})
export class EmployeeRoutingModule { }
