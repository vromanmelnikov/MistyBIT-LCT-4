import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Store } from '@ngrx/store';
import { Employee, Employeer } from 'src/app/shared/models/employers.model';
import { EmployeePipe } from 'src/app/shared/pipes/employee.pipe';
import EmployeeService from 'src/app/shared/services/employee.service';
import { setEmployyes } from 'src/app/store/manager.actions';
import { ChangeEmployeeDialogComponent } from './change-employee-dialog/change-employee-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { AddEmployyeDialogComponent } from '../add-employye-dialog/add-employye-dialog.component';
import { Grade, Office, Role } from 'src/app/shared/models/user.model';

@Component({
  selector: 'app-employeers-table',
  templateUrl: './employeers-table.component.html',
  styleUrls: ['./employeers-table.component.css'],
})
export class EmployeersTableComponent implements OnInit {
  @Input() role!: Role;
  @Input() allGrades: Grade[] = [];
  @Input() allOffices: Office[] = [];

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
    },
    {
      key: 'grade_name',
      viewValue: 'Грейд',
    },
    {
      key: 'office_address',
      viewValue: 'Офис',
    },
  ];

  columns: string[] = this.displayedColumns.map((column) => column.key);

  list: Employee[] = [];
  filteredList: Employee[] = [];

  expandedElement: Employeer | null = null;

  constructor(
    private store: Store<any>,
    private employeeService: EmployeeService,
    private dialog: MatDialog,
  ) {}

  ngOnInit(): void {
    // this.employeeService.getAllEmployees().subscribe((res: any) => {
    //   const items = new EmployeePipe().transform(res.items);
    //   this.store.dispatch(setEmployyes(items));
    //   this.list = items;
    //   this.filteredList = [...this.list];
    // });
    this.store.subscribe((res) => {
      this.list = res.manager.employeers;
      console.log(this.list);
      this.filteredList = [...this.list];
    });
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

  clickElement(element: Employeer) {
    this.expandedElement = this.expandedElement === element ? null : element;
  }

  change() {
    if (this.expandedElement) {
      this.dialog.open(ChangeEmployeeDialogComponent, {
        data: {
          employee: this.expandedElement,
          allGrades: this.allGrades,
          allOffices: this.allOffices,
        },
      });
    }
  }

  @Output('add') onAdding = new EventEmitter();

  add() {
    this.onAdding.emit();
  }
}
