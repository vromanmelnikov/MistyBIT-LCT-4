import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-date-item',
  templateUrl: './date-item.component.html',
  styleUrls: ['./date-item.component.css'],
})
export class DateItemComponent implements OnInit {
  @Input('item') dateItem: any;

  constructor() {}

  ngOnInit(): void {
  }
}
