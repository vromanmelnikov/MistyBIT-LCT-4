import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { Skill } from 'src/app/shared/models/employers.model';
import { SkillsPipe } from 'src/app/shared/pipes/skills.pipe';
import TaskService from 'src/app/shared/services/task.service';
import UserService from 'src/app/shared/services/user.service';

@Component({
  selector: 'app-task-item',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.css']
})
export class TaskComponent implements OnInit {
  @Input() item: any
  
  skills: Skill[] = []
  skillsCtrl = new FormControl();
  filteredSkills!: Observable<Skill[]>;

  panelOpenState: boolean = false

  constructor(private taskService: TaskService, private userService: UserService) { 
  }

  ngOnInit(): void {
    this.skills = new SkillsPipe().transform(this.item.skill_links)
  }

  @Output() onTaskDelete = new EventEmitter()

  deleteTask() {
    this.taskService.deleteTaskType(this.item.id).subscribe(
      res => {
        this.onTaskDelete.emit({id: this.item.id})
      }
    )
  }

}
