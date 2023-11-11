import { Component, Input, OnInit } from '@angular/core';
import { YaReadyEvent } from 'angular8-yandex-maps';
import { Coordinates } from '../../services/tasks.service';
import { Store } from '@ngrx/store';
import TaskService from '../../services/task.service';

@Component({
  selector: 'app-yandex-map',
  templateUrl: './yandex-map.component.html',
  styleUrls: ['./yandex-map.component.css'],
})
export class YandexMapComponent implements OnInit {
  @Input() points: Coordinates[] = [];

  map: ymaps.Map | null = null;
  coordTaskNow: any;
  employee_id: any;
  flag: any;
  constructor(
    private store: Store<any>,
    private taskService: TaskService,
  ) {}

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
            console.log(res);
            this.coordTaskNow = res.items[0].point.coordinate;
            this.flag = true;
          },
          (error) => {
            this.flag = false;
            this.coordTaskNow = { y: 38.977131, x: 45.044942 };
          },
        );
    });
  }

  ngOnInit(): void {
    this.loadTasks();
    this.taskService.ReloadTask.subscribe(() => {
      this.loadTasks();
      console.log('Task loaded');
    });
  }

  onMapReady(event: YaReadyEvent<ymaps.Map>): void {
    this.map = event.target;
  }
}
