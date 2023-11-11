import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-condition',
  templateUrl: './condition.component.html',
  styleUrls: ['./condition.component.css'],
})
export class ConditionComponent implements OnInit {
  @Input() index: number = -1;
  @Input() condition: any;

  conditionDesc: string = '';
  formula: any = {};

  form = new FormGroup({
    name: new FormControl(''),
  });

  subconditions: any[] = [];

  constructor() {}

  ngOnInit(): void {

    console.log(this.condition)

    this.form.setValue({ name: this.condition.description });

    this.subconditions = this.condition.subconditions;

    if (this.subconditions.length === 0) {
      this.addEmptySubcondition();
    }
  }

  @Output() onConditionAdd = new EventEmitter();

  onSubconditionAdd(data: any) {
    this.subconditions[data.index] = data.formulaItem;
    this.subconditions[data.index].isAdded = true;

    this.onConditionAdd.emit({
      index: this.index,
      conditionItem: {
        description: this.form.value.name,
        subconditions: this.subconditions,
      },
    });
    
    this.addEmptySubcondition();

    // if (data.isChanging === false) {
    //   this.addEmptySubcondition()
    // }
  }

  onBlur(event: any) {
    this.onConditionAdd.emit({
      index: this.index,
      conditionItem: {
        description: this.form.value.name,
        subconditions: this.subconditions,
      },
    });
  }

  addEmptySubcondition() {
    const empty = {
      key: '',
      value: {},
      isAdded: false,
    };
    this.subconditions.push(empty);
  }
}
