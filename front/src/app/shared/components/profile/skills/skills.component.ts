import { COMMA, ENTER } from '@angular/cdk/keycodes';
import {
  Component,
  ElementRef,
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

  constructor(
    private store: Store<any>,
    private employeeService: EmployeeService,
    private userService: UserService,
  ) {
    this.userService.getAllSkills().subscribe((res) => {
      const items: Skill[] = res.items;
      this.store.dispatch(SetAllSkillsAction(items));
    });
  }

  ngOnInit() {
    this.store.subscribe((res) => {
      let skills = new SkillsPipe().transform(res.user.skills);

      this.skills = skills;

      this.store.subscribe((static_res) => {
        this.allSkills = static_res.static.allSkills;

        this.filteredSkills = this.skillsCtrl.valueChanges.pipe(
          startWith(null),
          map((skill: string | Skill | null) =>
            skill ? this._filter(skill) : this.allSkills.slice(),
          ),
        );
      });
    });
  }

  add(event: MatChipInputEvent): void {
    // console.log(event)
    // const value = (event.value || '').trim();
    // console.log(value)
    // // // Add our skills
    // // if (value) {
    // //   this.skills.push(value);
    // // }
    // // // Clear the input value
    event.chipInput!.clear();
    this.skillsCtrl.setValue(null);
  }

  remove(id: number): void {
    this.userService.deleteSkill(id).subscribe((res) => {
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

    this.userService.addSkill(id).subscribe((res) => {
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
  }

  private _filter(skill: string | Skill): Skill[] {
    let filterValue = '';

    if (typeof skill === 'string') {
      filterValue = skill.toLowerCase();
    } else {
      //@ts-ignore
      filterValue = skill.name.toLowerCase();
    }

    const filteredSkills = this.allSkills.filter((skill) =>
      skill.name.toLowerCase().includes(filterValue),
    );

    return filteredSkills;
  }
}
