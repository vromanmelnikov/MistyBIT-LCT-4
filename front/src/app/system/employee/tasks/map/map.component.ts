import { Component, OnInit } from '@angular/core';
import TasksService from 'src/app/shared/services/tasks.service';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {

  points: any

  constructor(private tasksService: TasksService) { }

  ngOnInit(): void { 
    this.points = this.tasksService.points
  }

}
