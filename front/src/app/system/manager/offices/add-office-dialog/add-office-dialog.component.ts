import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Store } from '@ngrx/store';
import { PointsPipe } from 'src/app/shared/pipes/points.pipe';
import StaticService from 'src/app/shared/services/static.service';
import { SetPointsAction } from 'src/app/store/static.actions';

@Component({
  selector: 'app-add-office-dialog',
  templateUrl: './add-office-dialog.component.html',
  styleUrls: ['./add-office-dialog.component.css']
})
export class AddOfficeDialogComponent implements OnInit {

  form = new FormGroup({
    address: new FormControl('', []),
  });

  constructor(
    public dialogRef: MatDialogRef<AddOfficeDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private staticService: StaticService,
    private store: Store<any>
  ) {}

  ngOnInit(): void {}

  onNoClick(): void {
    const { address } = this.form.value;

    this.staticService.addOffice(<string>address).subscribe((res) => {

      // this.data.updateOffices()
      this.dialogRef.close();

      // this.staticService.getAllPoints().subscribe((res: any) => {
      //   if (res.items) {
      //     const items = new PointsPipe().transform(res.items);
      //     this.store.dispatch(SetPointsAction(items))
      //     this.dialogRef.close();
      //   }
      // });
    });
  }

}
