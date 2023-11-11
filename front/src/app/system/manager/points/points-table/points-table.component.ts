import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Store } from '@ngrx/store';
import { Point } from 'src/app/shared/models/points.model';
import { AddPointDialogComponent } from './add-point-dialog/add-point-dialog.component';
import StaticService from 'src/app/shared/services/static.service';
import { PointsPipe } from 'src/app/shared/pipes/points.pipe';
import { SetPointsAction } from 'src/app/store/static.actions';
import { ChangePointDialogComponent } from './change-point-dialog/change-point-dialog.component';

@Component({
  selector: 'app-points-table',
  templateUrl: './points-table.component.html',
  styleUrls: ['./points-table.component.css'],
})
export class PointsTableComponent implements OnInit {
  displayedColumns: any[] = [
    {
      key: 'address',
      viewValue: 'Адрес точки',
    },
    {
      key: 'created_at_conv',
      viewValue: 'Когда подключена точка?',
    },
    {
      key: 'is_delivered_card_conv',
      viewValue: 'Карты и материалы доставлены?',
    },
    {
      key: 'last_date_issue_card_conv',
      viewValue: 'Дата выдачи последней карты',
    },
    {
      key: 'quantity_requests',
      viewValue: 'Кол-во одобренных заявок',
    },
    {
      key: 'quantity_card',
      viewValue: 'Кол-во выданных карт',
    },
  ];

  columns: string[] = this.displayedColumns.map((column) => column.key);

  points: Point[] = [];

  expandedElement: Point | null = null;
  filteredList: Point[] = [];

  constructor(
    private store: Store<any>,
    private dialog: MatDialog,
    private staticService: StaticService,
  ) {}

  ngOnInit(): void {
    this.store.subscribe((res) => {
      const items = res.static.points;
      this.points = items;
      this.filteredList = this.points;
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value.toLowerCase();

    console.log(filterValue);

    if (filterValue === '') {
      this.filteredList = [...this.points];
    } else {
      this.filteredList = this.points.filter((item) =>
        item.address.toLowerCase().includes(filterValue),
      );
    }
  }

  clickElement(element: Point) {
    this.expandedElement = this.expandedElement === element ? null : element;
  }

  add() {
    this.dialog.open(AddPointDialogComponent, {
      data: {},
    });
  }

  change(event: any) {
    console.log(event)
    this.dialog.open(ChangePointDialogComponent, {
      data: {item: this.expandedElement, onPointDataChange: this.onPointDataChange},
    }).afterClosed().subscribe(res => {
      this.expandedElement = null
    })
  }

  onPointDataChange() {

    

  }

  deletePoint() {
    console.log(this.expandedElement);

    if (this.expandedElement) {
      const id = this.expandedElement!.id;
      this.staticService.deletePoint(id).subscribe((res) => {
        this.staticService.getAllPoints().subscribe((res: any) => {
          if (res.items) {
            const items = new PointsPipe().transform(res.items);
            this.store.dispatch(SetPointsAction(items));
            this.expandedElement = null;
          }
        });
      });
    }
  }
}
