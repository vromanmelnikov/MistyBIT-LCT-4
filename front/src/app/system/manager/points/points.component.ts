import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { PointsPipe } from 'src/app/shared/pipes/points.pipe';
import StaticService from 'src/app/shared/services/static.service';
import { SetPointsAction } from 'src/app/store/static.actions';

@Component({
  selector: 'app-points',
  templateUrl: './points.component.html',
  styleUrls: ['./points.component.css'],
})
export class PointsComponent implements OnInit {
  constructor(
    private store: Store<any>,
    private staticService: StaticService,
  ) {}

  ngOnInit(): void {
    this.staticService.getAllPoints().subscribe((res: any) => {
      if (res.items) {
        const items = new PointsPipe().transform(res.items);
        this.store.dispatch(SetPointsAction(items))
      }
    });
  }
}
