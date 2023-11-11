import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { Role } from '../../models/user.model';
import TaskService from '../../services/task.service';
import { TypeTaskGradePostModel, TypeTaskSkillPostModel } from '../../models/task.model';
import StaticService from 'src/app/shared/services/static.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'],
})
export class ProfileComponent implements OnInit {
  @Input() isManager: boolean = false;

  role: Role = {
    id: -1,
    name: 'Сотрудник',
    is_public: true,
  };

  constructor(
    private store: Store<any>,
    private router: Router,
    private http: HttpClient,
    private taskService: TaskService,
    private staticService: StaticService
  ) {
  }

  ngOnInit(): void {
    this.store.subscribe((res) => {
      this.role = res.user.profile.role
      // console.log(res)
    });
    // this.staticService.putPoint(1,"dsadas", {}).subscribe(
    //   (res: any) => {
    //     console.log(res)
    //   },
    //   (err) => {
    //     console.log(err)
    //   }
    // )
  }
  goToTasksList() {
    this.router.navigate(['/employee/tasks']);
  }
}
