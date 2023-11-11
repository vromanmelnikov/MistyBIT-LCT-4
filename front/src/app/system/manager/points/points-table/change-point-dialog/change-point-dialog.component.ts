import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Store } from '@ngrx/store';
import { lastValueFrom, of } from 'rxjs';
import { PointsPipe } from 'src/app/shared/pipes/points.pipe';
import StaticService from 'src/app/shared/services/static.service';
import TaskService from 'src/app/shared/services/task.service';
import { SetPointsAction } from 'src/app/store/static.actions';

@Component({
  selector: 'app-change-point-dialog',
  templateUrl: './change-point-dialog.component.html',
  styleUrls: ['./change-point-dialog.component.css'],
})
export class ChangePointDialogComponent implements OnInit {
  form = new FormGroup({
    quantity_requests: new FormControl(0),
    quantity_card: new FormControl(0),
    is_delivered_card: new FormControl(false)
  });

  constructor(
    public dialogRef: MatDialogRef<ChangePointDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private staticService: StaticService,
    private taskService: TaskService,
    private store: Store<any>,
  ) {}

  ngOnInit(): void {
    console.log(this.data.item)
  }

  async onNoClick() {
    const { quantity_card, quantity_requests } = this.form.value;

    let res_1,
      res_2 = null;

    if (<number>quantity_card > 0) {
      res_1 = await lastValueFrom(
        this.staticService.putPointQuantityCard(
          this.data.item.id,
          <number>quantity_card,
        ),
      );
    }

    if (<number>quantity_requests > 0) {
      res_2 = await lastValueFrom(
        this.staticService.putPointQuantityRequests(
          this.data.item.id,
          <number>quantity_requests,
        ),
      );
    }

    if (res_1 || res_2) {
      this.staticService.getAllPoints().subscribe((res: any) => {
        if (res.items) {
          const items = new PointsPipe().transform(res.items);
          this.store.dispatch(SetPointsAction(items))
        }
      });
    }
  }
}
function lastValue() {
  throw new Error('Function not implemented.');
}
