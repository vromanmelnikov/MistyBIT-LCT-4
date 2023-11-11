import { COMMA, ENTER, V } from '@angular/cdk/keycodes';
import {
  Component,
  ElementRef,
  Input,
  OnInit,
  ViewChild,
  inject,
} from '@angular/core';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import {
  MatAutocompleteSelectedEvent,
  MatAutocompleteModule,
} from '@angular/material/autocomplete';
import { MatChipInputEvent, MatChipsModule } from '@angular/material/chips';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import EmployeeService from 'src/app/shared/services/employee.service';
import { Skill } from 'src/app/shared/models/employers.model';
import UserService from 'src/app/shared/services/user.service';
import { Store } from '@ngrx/store';
import { SkillsPipe } from 'src/app/shared/pipes/skills.pipe';
import { SetAllSkillsAction } from 'src/app/store/static.actions';
import TaskService from 'src/app/shared/services/task.service';
import { showMessage } from 'src/app/shared/common';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-skills',
  templateUrl: './skills.component.html',
  styleUrls: ['./skills.component.css'],
})
export class SkillsComponent implements OnInit {
  separatorKeysCodes: number[] = [ENTER, COMMA];

  allSkills: Skill[] = [];

  skillsCtrl = new FormControl();
  filteredSkills!: Observable<Skill[]>;

  skills: Skill[] = [];

  @ViewChild('skillsInput') skillsInput!: ElementRef<HTMLInputElement>;

  @Input('skills') task_skills: Skill[] = [];
  @Input() type_task_id: number = -1;
  // @Input()

  constructor(
    private taskService: TaskService,
    private userService: UserService,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit(): void {
    this.skills = this.task_skills;
    this.userService.getAllSkills().subscribe((res) => {
      const items: Skill[] = res.items;
      this.allSkills = items;
      this.filteredSkills = this.skillsCtrl.valueChanges.pipe(
        startWith(null),
        map((skill: string | Skill | null) =>
          skill ? this._filter(skill) : this.allSkills.slice(),
        ),
      );
    });
  }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();
    if (value !== '') {
      this.userService.addNewSkill(value).subscribe((res) => {  

        showMessage(this.snackBar, 'Новый навык добавлен!');

        this.userService.getAllSkills().subscribe((res) => {
          const items: Skill[] = res.items;
          this.allSkills = items;
          this.filteredSkills = this.skillsCtrl.valueChanges.pipe(
            startWith(null),
            map((skill: string | Skill | null) =>
              skill ? this._filter(skill) : this.allSkills.slice(),
            ),
          );
          const newSkillID = this.allSkills.filter((item: Skill) => item.name === value)[0].id
          this.skills.push({
            id: newSkillID,
            name: value,
          });
        });
      });
    }
    // // // Add our skills
    // // if (value) {
    // //   this.skills.push(value);
    // // }
    // // // Clear the input value
    event.chipInput!.clear();
    this.skillsCtrl.setValue(null);
  }

  remove(id: number): void {
    this.taskService
      .deleteTaskTypeSkill({ type_task_id: this.type_task_id, skill_id: id })
      .subscribe((res) => {
        this.skills = this.skills.filter((skill) => skill.id != id);
        this.filteredSkills = this.skillsCtrl.valueChanges.pipe(
          startWith(null),
          map((skill: string | Skill | null) =>
            skill ? this._filter(skill) : this.allSkills.slice(),
          ),
        );
      });
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    const id = event.option.value.id;
    this.taskService
      .addTaskTypeSkill({ type_task_id: this.type_task_id, skill_id: id })
      .subscribe((res) => {
        this.skills.push(event.option.value);
        this.skillsInput.nativeElement.value = '';
        this.skillsCtrl.setValue(null);
        this.filteredSkills = this.skillsCtrl.valueChanges.pipe(
          startWith(null),
          map((skill: string | Skill | null) =>
            skill ? this._filter(skill) : this.allSkills.slice(),
          ),
        );
      });
    // this.userService.addSkill(id).subscribe((res) => {
    //   this.skills.push(event.option.value);
    //   this.skillsInput.nativeElement.value = '';
    //   this.skillsCtrl.setValue(null);
    //   this.filteredSkills = this.skillsCtrl.valueChanges.pipe(
    //     startWith(null),
    //     map((skill: string | Skill | null) =>
    //       skill ? this._filter(skill) : this.allSkills.slice(),
    //     ),
    //   );
    // });
  }

  private _filter(skill: string | Skill): Skill[] {
    let filterValue = '';

    console.log(skill);

    if (typeof skill === 'string') {
      filterValue = skill.toLowerCase();
    } else {
      filterValue = skill.name.toLowerCase();
    }

    const filteredSkills = this.allSkills.filter((skill) =>
      skill.name.toLowerCase().includes(filterValue),
    );

    return filteredSkills;
  }
}
