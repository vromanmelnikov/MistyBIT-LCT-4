import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';

@Component({
  selector: 'app-employee',
  templateUrl: './employee.component.html',
  styleUrls: ['./employee.component.css', '../../shared/shared.component.css']
})
export class EmployeeComponent implements OnInit {

  constructor(
    private store: Store<any>,
    private router: Router,
  ) {
    this.store.subscribe((res) => {
      const role = res.user.profile.role.name;

      // console.log(role)

      // if (role === 'Менеджер') {
      //   this.router.navigate(['/manager/profile']);
      // }
    });
  }

  ngOnInit(): void {
  }

}
