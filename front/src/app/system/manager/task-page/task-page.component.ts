import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { map, startWith } from 'rxjs';
import { SelectInput } from 'src/app/shared/models/input.model';
import EmployeeService from 'src/app/shared/services/employee.service';
import StaticService from 'src/app/shared/services/static.service';
import TaskService from 'src/app/shared/services/task.service';

@Component({
  selector: 'app-task-page',
  templateUrl: './task-page.component.html',
  styleUrls: ['./task-page.component.css'],
})
export class TaskPageComponent implements OnInit {
  constructor(
    private taskService: TaskService,
    private staticService: StaticService,
    private emplService: EmployeeService,
    private _snackBar: MatSnackBar,
  ) {}
  tasks: any;
  allStatuses: any;
  types: any;
  points: any;
  employees: any[] = [];
  priorities: any;
  ngOnInit(): void {
    this.taskService
      .getTasksAll(
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
      )
      .subscribe((res: any) => {
        this.tasks = res.items;
      });
    this.taskService.getStatusesAll(false).subscribe((res: any) => {
      this.allStatuses = res.items;
      this.statusInput.icon = 'keyboard_arrow_down';
      this.statusInput.values = this.compile_values('status', this.allStatuses);
    });
    this.taskService.getTasksTypes().subscribe((res: any) => {
      this.types = res.items;
      this.typeInput.icon = 'keyboard_arrow_down';
      this.typeInput.values = this.compile_values('type', this.types);
    });
    this.staticService.getAllPoints().subscribe((res: any) => {
      this.points = res.items;
      this.pointInput.icon = 'keyboard_arrow_down';
      this.pointInput.values = this.compile_values('point', this.points);
    });
    this.emplService.getAllEmployees().subscribe((res: any) => {
      for (let item of res.items) {
        item.name = `${item.user.lastname} ${item.user.firstname} ${item.user.patronymic}`;
        this.employees.push(item);
      }
      this.employeeInput.icon = 'keyboard_arrow_down';
      this.employeeInput.values = this.compile_values(
        'employee',
        this.employees,
      );
    });
    this.taskService.getPrioritiesAll().subscribe((res: any) => {
      this.priorities = res.items;
      this.priorityInput.icon = 'keyboard_arrow_down';
      this.priorityInput.values = this.compile_values(
        'priority',
        this.priorities,
      );
    });
  }
  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      horizontalPosition: 'center',
      verticalPosition: 'top',
      duration: 5000,
    });
  }
  form = new FormGroup({
    type: new FormControl(null),
    point: new FormControl(null),
    status: new FormControl(null),
    priority: new FormControl(null),
    employee: new FormControl(null),
  });
  typeInput: SelectInput = {
    field: 'type',
    type: 'text',
    label: 'Загрузка типов...',
    formControl: this.form.get('type'),
  };
  pointInput: SelectInput = {
    field: 'point',
    type: 'text',
    label: 'Загрузка точек...',
    formControl: this.form.get('point'),
  };
  statusInput: SelectInput = {
    field: 'status',
    type: 'text',
    label: 'Загрузка статусов...',
    formControl: this.form.get('status'),
  };
  priorityInput: SelectInput = {
    field: 'priority',
    type: 'text',
    label: 'Загрузка приоритетов...',
    formControl: this.form.get('priority'),
  };
  employeeInput: SelectInput = {
    field: 'employee',
    type: 'text',
    label: 'Загрузка сотрудников...',
    formControl: this.form.get('employee'),
  };
  private _filterValues(value: any, items: any[]) {
    return items.filter((item) =>
      item.name.toLowerCase().includes(value.toLowerCase()),
    );
  }

  compile_values(name: string, arr: any[]) {
    return this.form.get(name)?.valueChanges.pipe(
      startWith(''),
      map((value) => (value ? this._filterValues(value, arr) : arr.slice())),
    );
  }
  getStatusTask(status_id: number) {
    const status = this.allStatuses.filter(function (item: any) {
      return item.id == status_id;
    });
    return status[0].name;
  }
  defineTask() {
    this.taskService.taskDelete().subscribe((res: any) => {
      this.taskService.addTaskDefine().subscribe((res: any) => {
        this.taskService
          .addTaskDistribution(undefined, undefined)
          .subscribe((res: any) => {
            this.openSnackBar(res.message, 'OK');
            this.taskService.getTasksAll().subscribe((res: any) => {
              this.tasks = res.items;
            });
          });
      });
    });
  }
  applyFilter() {
    const { type, point, status, priority, employee } = this.form.value;
    let type_id = undefined;
    let point_id = undefined;
    let status_id = undefined;
    let priority_id = undefined;
    let employee_id = undefined;
    if (type != undefined && type != '') {
      type_id = this.types.find((i: any) => i.name == type).id;
    }
    if (point != undefined && point != '') {
      point_id = this.points.find((i: any) => i.address == point).id;
    }
    if (status != undefined && status != '') {
      status_id = this.allStatuses.find((i: any) => i.name == status).id;
    }
    if (priority != undefined && priority != '') {
      priority_id = this.priorities.find((i: any) => i.name == priority).id;
    }
    if (employee != undefined && employee != '') {
      employee_id = this.employees.find((i: any) => i.name == employee).id;
    }

    console.log(type_id, point_id, status_id, priority_id);
    this.taskService
      .getTasksAll(
        undefined,
        undefined,
        type_id,
        point_id,
        status_id,
        priority_id,
        employee_id,
        undefined,
        undefined,
      )
      .subscribe((res: any) => {
        this.tasks = res.items;
      });
  }

  download() {
    //@ts-ignore
    this.taskService.getReport().subscribe((res: any) => {
      let data = res.body;
      const url = window.URL.createObjectURL(res.body as any);
      const a = document.createElement('a');
      a.href = url;
      let name: any = res.headers.get('content-disposition').split('"')
      name = name[name.length - 2]
      a.download = name;
      a.click();
      window.URL.revokeObjectURL(url);
    })
  }
}
