import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Employee } from 'src/app/shared/models/employers.model';
import { Office } from 'src/app/shared/models/user.model';
import { EmployeePipe } from 'src/app/shared/pipes/employee.pipe';
import EmployeeService from 'src/app/shared/services/employee.service';
import StaticService from 'src/app/shared/services/static.service';

@Component({
  selector: 'app-office',
  templateUrl: './office.component.html',
  styleUrls: ['./office.component.css'],
})
export class OfficeComponent implements OnInit {

  panelOpenState: boolean = false

  @Input() office!: Office;
  list: Employee[] = [];

  changing: boolean = false

  form = new FormGroup({
    address: new FormControl('', [])
  })

  constructor(private employeeService: EmployeeService, private staticService: StaticService) {}

  ngOnInit(): void {

    this.form.setValue({address: this.office.address})

    this.employeeService
      .getAllEmployees(this.office.id)
      .subscribe((res: any) => {
        if (res.items) {
          this.list = new EmployeePipe().transform(res.items);
        }
      });
  }

  @Output() onOfficeChange: EventEmitter<{id: number, address: any}> = new EventEmitter()

  changeAddress() {
    const {address} = this.form.value
    this.staticService.changeOfficeAddress(this.office.id, <string>address).subscribe(
      res => {

        this.onOfficeChange.emit({id: this.office.id, address})

        this.changing = false
      }
    )
  }

  @Output() onDelete = new EventEmitter()

  deleteOffice() {
    this.staticService.deleteOffice(this.office.id).subscribe(
      res => {
        this.onDelete.emit()
      }
    )
  }

}
