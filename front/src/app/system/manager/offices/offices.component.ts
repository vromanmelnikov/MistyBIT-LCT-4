import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Office } from 'src/app/shared/models/user.model';
import StaticService from 'src/app/shared/services/static.service';
import { AddOfficeDialogComponent } from './add-office-dialog/add-office-dialog.component';

@Component({
  selector: 'app-offices',
  templateUrl: './offices.component.html',
  styleUrls: ['./offices.component.css'],
})
export class OfficesComponent implements OnInit {
  panelOpenState: boolean = true;

  offices: Office[] = [];

  constructor(private staticService: StaticService, private dialog: MatDialog) {}

  ngOnInit(): void {
    this.updateOffices()
  }

  onOfficeChange(event: {id: number, address: any}) {
    this.offices = this.offices.map((item) => {
      const newItem = item;
      if (item.id === event.id) {
        newItem.address = event.address;
      }

      return newItem;
    });
  }

  add() {
    this.dialog.open(AddOfficeDialogComponent).afterClosed().subscribe(
      res => {
        this.updateOffices()
      }
    )
  }

  updateOffices() {
    console.log('туть')
    this.staticService.getAllOffices().subscribe((res) => {
      if (res.items) {
        this.offices = res.items;
      }
    });
  }

  onDelete(event: any) {
    this.updateOffices()
  }
}
