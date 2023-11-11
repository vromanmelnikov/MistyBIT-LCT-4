import StaticService from 'src/app/shared/services/static.service';
import { Component, OnInit } from '@angular/core';
import SecurityService from 'src/app/shared/services/security.service';
import { Store } from '@ngrx/store';
import { Router } from '@angular/router';
import { showMessage } from 'src/app/shared/common';
import { MatSnackBar } from '@angular/material/snack-bar';

const ADMIN_ID = 3;

@Component({
  selector: 'app-security',
  templateUrl: './security.component.html',
  styleUrls: ['./security.component.css'],
})
export class SecurityComponent implements OnInit {
  constructor(
    private _snackBar: MatSnackBar,
    private securityService: SecurityService,
    private staticService: StaticService,
    private store: Store<any>,
    private router: Router,
  ) {}

  methods: any[] = [];
  roles: any[] = [];

  openPolicies(method: any) {
    if (!method.policy) {
      this.securityService
        .getPolicyMethod(method.action, method.resource)
        .subscribe((res: any) => {
          method.policy = res[0];

          let roles: any[] = [];
          this.roles.forEach((role: any) => {
            let findSub = method.policy.subjects.filter(
              (subject: any) => subject.role_id == role.id,
            );

            let checked = findSub.length > 0;
            roles.push({
              name: role.name,
              id: role.id,
              checked: checked,
              isOwner: checked
                ? findSub[0].is_owner
                  ? findSub[0].is_owner
                  : false
                : false,
            });
          });

          method.policy.allRoles = roles;
          // });
        });
    }
  }

  resetSlideToggle(role: any) {
    if (role.checked) {
      role.isOwner = false;
    }
  }

  savePolicy(method: any) {
    let subjects: any[] = [];
    method.policy.allRoles.forEach((role: any) => {
      if (role.checked) {
        let sub: any = { role_id: role.id };
        if (role.isOwner) {
          sub.is_owner = role.isOwner;
        }
        subjects.push(sub);
      }
    });
    this.securityService
      .updatePolicy({
        uid: method.policy.uid,
        description: method.policy.description,
        subjects: subjects,
      })
      .subscribe(
        (res) => {
          console.log(res);
        },
        (err) => {
          console.log(err);
        },
      );
  }

  ngOnInit() {
    this.store.subscribe((res) => {
      const user = res.user.profile;

      if (user.role_id == ADMIN_ID) {
        this.securityService.getSecurityMethods().subscribe((methods: any) => {
          this.methods = methods;
        });
        this.staticService.getAllRoles().subscribe((roles: any) => {
          this.roles = roles.items;
        });
      } else {
        this.router.navigate(['/manager/profile']);
        showMessage(this._snackBar, 'Доступно только администратору');
      }
    });
  }
}
