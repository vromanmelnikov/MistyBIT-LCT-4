import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from 'src/app/shared/services/auth.service';

@Component({
  selector: 'app-reset',
  templateUrl: './reset.component.html',
  styleUrls: ['./reset.component.css'],
})
export class ResetComponent implements OnInit {
  form = new FormGroup({
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
    ]),
  });

  code: string = '';

  constructor(
    private authService: AuthService,
    private activateRoute: ActivatedRoute,
    private router: Router,
  ) {
    this.activateRoute.queryParams.subscribe((params) => {
      this.code = params['code'];
    });
  }

  ngOnInit(): void {}

  reset() {
    const { password } = this.form.value;

    this.authService
      .ResetPassword(this.code, <string>password)
      .subscribe((res) => {
        this.router.navigate(['/auth/login']);
      });
  }
}
