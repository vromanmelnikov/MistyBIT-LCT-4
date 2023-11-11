import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-item',
  templateUrl: './item.component.html',
  styleUrls: ['./item.component.css'],
})
export class ItemComponent implements OnInit {
  @Input() item: any;

  panelOpenState: boolean = false;

  fulledStars!: any[];
  stars!: any[];

  constructor() {}

  ngOnInit(): void {
    this.fulledStars = Array.from(Array(this.item.mark));
    this.stars = Array.from(Array(5 - this.item.mark));
  }
}
