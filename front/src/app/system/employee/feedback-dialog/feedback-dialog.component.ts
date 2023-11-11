import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

interface FeedbackDialogData {
  stars: number;
  description: string;
}

@Component({
  selector: 'app-feedback-dialog',
  templateUrl: './feedback-dialog.component.html',
  styleUrls: ['./feedback-dialog.component.css'],
})
export class FeedbackDialogComponent {
  stars: boolean[] = [false, false, false, false, false];
  comment: string = '';

  constructor(
    public dialogRef: MatDialogRef<FeedbackDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: FeedbackDialogData,
  ) {}

  onNoClick(): void {
    let i = 0;
    this.stars.forEach((star) => {
      if (star) i += 1;
    });
    this.data.stars = i;
    this.data.description = this.comment;
    this.dialogRef.close(this.data);
  }

  clickOnStar(index: number) {
    this.stars = this.stars.map((item: boolean, i: number) => {
      if (i < index) {
        return true;
      } else if (i === index && item === false) {
        return true;
      } else if (i === index && item === true) {
        return false;
      } else {
        return false;
      }
    });
  }
}
