import { Component, OnInit } from '@angular/core';
import { Skill } from 'src/app/shared/models/employers.model';
import { SkillsPipe } from 'src/app/shared/pipes/skills.pipe';
import TaskService from 'src/app/shared/services/task.service';
import UserService from 'src/app/shared/services/user.service';

@Component({
  selector: 'app-task-list',
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css'],
})
export class TaskListComponent implements OnInit {

  items: any[] = []

  constructor(private taskServices: TaskService, private userService: UserService) {}

  ngOnInit(): void {
    this.taskServices.getTasksTypes().subscribe((res: any) => {
      const items = res.items;
      this.items = items
    });
  }

  onTaskDelete(event: any) {
    this.items = this.items.filter((item: any) => item.id != event.id)
  }

}
