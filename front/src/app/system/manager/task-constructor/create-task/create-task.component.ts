import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { concatMap, finalize, from } from 'rxjs';
import EmployeeService from 'src/app/shared/services/employee.service';
import StaticService from 'src/app/shared/services/static.service';
import TaskService from 'src/app/shared/services/task.service';
import UserService from 'src/app/shared/services/user.service';

@Component({
  selector: 'app-create-task',
  templateUrl: './create-task.component.html',
  styleUrls: ['./create-task.component.css'],
})
export class CreateTaskComponent implements OnInit {
  allPriorites: any[] = [];
  allGrades: any[] = []

  form = new FormGroup({
    name: new FormControl(''),
    duration: new FormControl(''),
    interval_block: new FormControl(''),
    priority: new FormControl('')
  });

  grades = new FormControl()

  conditions: any[] = [];

  constructor(
    private staticService: StaticService,
    private taskService: TaskService,
    // private staticService: StaticService,
    // private emplService: EmployeeService
  ) {}

  ngOnInit(): void {
    this.taskService.getPrioritiesAll().subscribe((res: any) => {
      this.allPriorites = res.items;
      // console.log(this.allPriorites);
    });
    this.staticService.getAllGrades().subscribe((res: any) => {
      this.allGrades = res.items
    })
  }

  addCondition() {
    this.conditions.push({
      description: '',
      subconditions: [],
    });
  }

  onConditionAdd(data: any) {
    // console.log('Добавлено условие', data);
    this.conditions[data.index] = data.conditionItem;
    // this.addCondition()
  }

  createTask() {
    const conditions = this.conditions.map((condition: any) => {
      let formula: any = {};

      for (let subcondition of condition.subconditions) {
        if (subcondition.isAdded) {
          formula[subcondition.key] = subcondition.value;
        }
      }

      return {
        description: condition.description,
        formula,
      };
    });

    const { name, duration, interval_block, priority } = this.form.value;

    const priority_id = JSON.parse(<string>priority).id;

    const task: any = {
      name,
      duration,
      interval_block,
      priority_id,
      details: {},
      conditions
    };

    this.taskService.addTaskType(task).subscribe((res: any) => {
      const grades = this.grades.value.map(
        (item: any) => {
          const grade = this.allGrades.filter((grade: any) => grade.name === item)[0]
          return grade
        }
      )
      .map((grade: any) => this.taskService.addTaskTypeGrade({grade_id: grade.id, type_task_id: res.message}));
      
      from(grades)
          .pipe(
              concatMap((res: any) => res)
          ).subscribe((res) => { 
            console.log(res)
          });
              
    });
  }

  JSONtoString(object: any) {
    return JSON.stringify(object);
  }
}
