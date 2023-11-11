import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

interface ErrorDialogData {
  description: string;
}

@Component({
  selector: 'app-error-dialog',
  templateUrl: './error-dialog.component.html',
  styleUrls: ['./error-dialog.component.css'],
})
export class ErorrDialogComponent {
  description: string = '';

  constructor(
    public dialogRef: MatDialogRef<ErorrDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ErrorDialogData,
  ) {}

  onNoClick(): void {
    // let i = 0;
    // this.stars.forEach((star) => {
    //   if (star) i += 1;
    // });
    // this.data.stars = i;
    this.data.description = this.description;
    this.dialogRef.close(this.data);
  }

  // clickOnStar(index: number) {
  //   this.stars = this.stars.map((item: boolean, i: number) => {
  //     if (i < index) {
  //       return true;
  //     } else if (i === index && item === false) {
  //       return true;
  //     } else if (i === index && item === true) {
  //       return false;
  //     } else {
  //       return false;
  //     }
  //   });
  // }
}
