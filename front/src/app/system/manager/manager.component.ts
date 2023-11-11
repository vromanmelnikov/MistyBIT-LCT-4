import { Location } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';

@Component({
  selector: 'app-manager',
  templateUrl: './manager.component.html',
  styleUrls: ['./manager.component.css', '../../shared/shared.component.css'],
})
export class ManagerComponent implements OnInit {
  constructor(
    private store: Store<any>,
    private router: Router,
  ) {
    this.store.subscribe((res) => {
      const role = res.user.profile.role.name;

      if (role === 'Сотрудник') {
        this.router.navigate(['/employee/profile']);
      }
    });
  }

  ngOnInit(): void {}
}
