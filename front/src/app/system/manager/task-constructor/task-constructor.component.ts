import { Component, OnInit } from '@angular/core';
import StaticService from 'src/app/shared/services/static.service';
import TaskService from 'src/app/shared/services/task.service';

@Component({
  selector: 'app-task-constructor',
  templateUrl: './task-constructor.component.html',
  styleUrls: ['./task-constructor.component.css'],
})
export class TaskConstructorComponent implements OnInit {
  constructor(private staticService: StaticService) {}

  ngOnInit(): void {
    
  }
}
