import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import TaskService from 'src/app/shared/services/task.service';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css'],
})
export class ListComponent implements OnInit {
  remainsList: any[] = [];
  completedList: any[] = [];
  employee_id: any;

  constructor(
    private taskService: TaskService,
    private store: Store<any>,
  ) {}
  archiveFlag: boolean = false;
  checkTasks(is_remains: boolean = false) {
    if (is_remains) return this.remainsList.length > 0;
    else return this.completedList.length > 0;
  }
  onFlagChange(value: any) {
    this.archiveFlag = value;
  }
  loadTasks() {
    this.store.subscribe((res) => {
      this.employee_id = res.user.profile.id;
      this.taskService
        .getTasksAll(
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
          this.employee_id,
          undefined,
          undefined,
          false,
        )
        .subscribe(
          (res: any) => {
            this.remainsList = res.items;
          },
          (err) => {
            this.remainsList = err.items;
          },
        );
      this.taskService
        .getTasksHistoryAll(undefined, undefined, this.employee_id)
        .subscribe(
          (res: any) => {
            this.completedList = res.items;
          },
          (err) => {
            this.completedList = err.items;
          },
        );
    });
  }

  ngOnInit(): void {
    // this.remainsList = this.tasksService.employeerTasks.remainsList;
    // this.completedList = this.tasksService.employeerTasks.completedList;
    this.loadTasks();
    this.taskService.ReloadTask.subscribe(() => {
      console.log('Task loaded');
      this.loadTasks();
    });
  }
}
