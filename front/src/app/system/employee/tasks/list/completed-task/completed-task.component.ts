import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-completed-task',
  templateUrl: './completed-task.component.html',
  styleUrls: ['./completed-task.component.css']
})
export class CompletedTaskComponent implements OnInit {

  @Input() item: any

  fulledStars!: any[];
  stars!: any[];

  constructor() { }

  panelOpenState: boolean = false

  ngOnInit(): void {
  
    console.log(this.item)

    this.fulledStars = Array.from(Array(this.item.feedback_value));
    this.stars = Array.from(Array(5 - this.item.feedback_value));
  }

}
