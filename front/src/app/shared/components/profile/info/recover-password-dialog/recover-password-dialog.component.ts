import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

interface RecoverPasswordDialogData {
  id: number
}

@Component({
  selector: 'app-recover-password-dialog',
  templateUrl: './recover-password-dialog.component.html',
  styleUrls: ['./recover-password-dialog.component.css']
})
export class RecoverPasswordDialogComponent implements OnInit {

  constructor(
    public dialogRef: MatDialogRef<RecoverPasswordDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: RecoverPasswordDialogData,) { }

  ngOnInit(): void {
    console.log(this.data)
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

}
