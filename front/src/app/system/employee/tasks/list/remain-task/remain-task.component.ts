import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-remain-task',
  templateUrl: './remain-task.component.html',
  styleUrls: ['./remain-task.component.css']
})
export class RemainTaskComponent implements OnInit {

  @Input() item: any

  constructor() { }

  panelOpenState: boolean = false

  ngOnInit(): void {
  }

}
