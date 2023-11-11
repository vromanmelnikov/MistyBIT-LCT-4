import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Manager } from 'src/app/shared/models/employers.model';
import {
  animate,
  state,
  style,
  transition,
  trigger,
} from '@angular/animations';
import { Store, StoreRootModule } from '@ngrx/store';
import EmployeeService from 'src/app/shared/services/employee.service';
import { MatDialog } from '@angular/material/dialog';
import { EmployeePipe } from 'src/app/shared/pipes/employee.pipe';
import { Role } from 'src/app/shared/models/user.model';
import { ChangeManagerDialogComponent } from './change-manager-dialog/change-manager-dialog.component';

@Component({
  selector: 'app-managers-table',
  templateUrl: './managers-table.component.html',
  styleUrls: ['./managers-table.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition(
        'expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)'),
      ),
    ]),
  ],
})
export class ManagersTableComponent implements OnInit {

  @Input() role!: Role

  displayedColumns: any[] = [
    {
      key: 'lastname',
      viewValue: 'Фамилия',
    },
    {
      key: 'firstname',
      viewValue: 'Имя',
    },
    {
      key: 'patronymic',
      viewValue: 'Отчество',
    },
    {
      key: 'email',
      viewValue: 'Почта',
    }
  ];

  columns: string[] = this.displayedColumns.map((column) => column.key);

  list: Manager[] = [];
  filteredList: Manager[] = [];

  expandedElement: Manager | null = null;

  constructor(
    private store: Store<any>,
    private employeeService: EmployeeService,
    private dialog: MatDialog,
  ) {}

  async ngOnInit(): Promise<void> {
    const allManagersResponce = await this.employeeService.getAllmanagers();
    allManagersResponce.subscribe((res: any) => {
      if (res.items) {
        const items = res.items;
        // this.store.dispatch(setEmployyes(items));
        this.list = items;
        this.filteredList = [...this.list];
      }
    });

    // this.employeeService.getAllEmployees().subscribe((res: any) => {
    //   const items = new EmployeePipe().transform(res.items);
    //   // this.store.dispatch(setEmployyes(items));
    //   this.list = items;
    //   this.filteredList = [...this.list];
    // });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value.toLowerCase();

    if (filterValue === '') {
      this.filteredList = [...this.list];
    } else {
      this.filteredList = this.list.filter((item) => {
        const lastname = item.lastname.toLowerCase();
        const firstname = item.firstname.toLowerCase();
        const patronymic = item.patronymic.toLowerCase();
        const email = item.email.toLowerCase();

        if (
          lastname.includes(filterValue) ||
          firstname.includes(filterValue) ||
          patronymic.includes(filterValue) ||
          email.includes(filterValue)
        ) {
          return true;
        } else {
          return false;
        }
      });
    }
  }

  clickElement(element: Manager) {
    this.expandedElement = this.expandedElement === element ? null : element;
  }

  change() {
    if (this.expandedElement) {
      this.dialog.open(ChangeManagerDialogComponent, {
        data: { manager: this.expandedElement},
      });
    }
  }

  @Output('add') onAdding = new EventEmitter();

  add() {
    this.onAdding.emit();
  }
}
