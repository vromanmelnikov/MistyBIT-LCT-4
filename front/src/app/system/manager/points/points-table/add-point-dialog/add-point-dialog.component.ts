import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Store } from '@ngrx/store';
import { PointsPipe } from 'src/app/shared/pipes/points.pipe';
import StaticService from 'src/app/shared/services/static.service';
import { WebSocketService } from 'src/app/shared/services/websockets.service';
import { SetPointsAction } from 'src/app/store/static.actions';

@Component({
  selector: 'app-add-point-dialog',
  templateUrl: './add-point-dialog.component.html',
  styleUrls: ['./add-point-dialog.component.css'],
})
export class AddPointDialogComponent implements OnInit {
  form = new FormGroup({
    address: new FormControl('', []),
  });

  constructor(
    public dialogRef: MatDialogRef<AddPointDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private staticService: StaticService,
    private store: Store<any>
  ) {}

  ngOnInit(): void {}

  onNoClick(): void {
    const { address } = this.form.value;

    this.staticService.addPoint(<string>address).subscribe((res) => {

      // this.wsService.SendMessage({text: 'Сервис подсчитывает точки'})

      this.staticService.countWeights(true).subscribe(
        (res) => {
          console.log(res)
        }
      )

      this.staticService.getAllPoints().subscribe((res: any) => {
        if (res.items) {
          const items = new PointsPipe().transform(res.items);
          this.store.dispatch(SetPointsAction(items))
          this.dialogRef.close();
        }
      });
    });
  }
}
