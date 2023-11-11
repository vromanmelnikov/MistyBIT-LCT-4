import { Component, DoCheck, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Employeer, Manager } from 'src/app/shared/models/employers.model';
import EmployeersManagmentService from 'src/app/shared/services/employeers-managment.service';
import StaticService from 'src/app/shared/services/static.service';
import { AddEmployyeDialogComponent } from './add-employye-dialog/add-employye-dialog.component';
import { Store } from '@ngrx/store';
import { Grade, Office, Role } from 'src/app/shared/models/user.model';
import EmployeeService from 'src/app/shared/services/employee.service';
import { EmployeePipe } from 'src/app/shared/pipes/employee.pipe';
import { setEmployyes } from 'src/app/store/manager.actions';

interface EmployeerOption {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'app-employeers',
  templateUrl: './employeers.component.html',
  styleUrls: [
    './employeers.component.css',
    '../../../shared/shared.component.css',
  ],
})
export class EmployeersComponent implements OnInit, DoCheck {
  allGrades: Grade[] = [];
  allOffices: Office[] = [];
  allRoles: Role[] = [];

  constructor(
    private empMngmtService: EmployeersManagmentService,
    private staticService: StaticService,
    private dialog: MatDialog,
    private employeeService: EmployeeService,
    private store: Store<any>
  ) {}

  employeersTypes: EmployeerOption[] = [
    { value: 'employeer', viewValue: 'Выездные сотрудники' },
    { value: 'manager', viewValue: 'Менеджеры' },
  ];

  role!: Role

  archiveFlag: boolean = false;

  currentType: string = '';

  public employeersList: Employeer[] = [];
  public managersList: Manager[] = [];

  public employeersDisplayedColumns =
    this.empMngmtService.employeersDisplayedColumns;
  public managersDisplayedColumns =
    this.empMngmtService.managersDisplayedColumns;

  ngOnInit(): void {

    this.employeeService.getAllEmployees().subscribe((res: any) => {
      console.log('туть', res)
      const items = new EmployeePipe().transform(res.items);
      this.store.dispatch(setEmployyes(items));
    });

    this.store.subscribe(
      res => {
        this.role = res.user.profile.role
      }
    )

    this.currentType = this.employeersTypes[0].value;

    this.employeersList = this.empMngmtService.employeers;
    this.managersList = this.empMngmtService.managers;

    this.staticService.getAllGrades().subscribe((res: any) => {
      if (res.items) {
        const items = res.items;
        this.allGrades = items;
      }
      this.staticService.getAllOffices().subscribe((res: any) => {
        if (res.items) {
          const items = res.items;
          this.allOffices = items;
          this.staticService.getAllRoles().subscribe((res: any) => {
            if (res.items) {
              const items = res.items;
              this.allRoles = items;
            }
          });
        }
      });
    });
  }

  ngDoCheck(): void {}

  onFlagChange(value: any) {
    this.archiveFlag = value;
  }

  add(event: any) {

    this.dialog.open(AddEmployyeDialogComponent, {
      data: {
        allRoles: this.allRoles,
        allOffices: this.allOffices,
        allGrades: this.allGrades
      },
    });
    
  }
}
