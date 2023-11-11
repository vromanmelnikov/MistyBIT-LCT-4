import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import StaticService from 'src/app/shared/services/static.service';
import TaskService from 'src/app/shared/services/task.service';

@Component({
  selector: 'app-subcondition',
  templateUrl: './subcondition.component.html',
  styleUrls: ['./subcondition.component.css'],
})
export class SubconditionComponent implements OnInit {
  @Input() index: number = -1;
  @Input() isAdded: boolean = true;
  @Input() subcondition: any;

  selectedType: any;

  allConditionTypes: any[] = [];

  pointParams: any[] = [];
  pointConditionTypes: any[] = [];

  pointConditionType: string = '';
  selectedConditionType: any;
  selectedConditionParam_1: any;
  selectedConditionParam_2: any;
  selectTypeOfResult: any;
  conditionValue: any;

  selectedParam: any;
  conditionTypes: any[] = [];
  conditionParams_1: any[] = [];
  conditionParams_2: any[] = [];
  conditionResultTypes: any[] = [];

  onConditionParam_1_Change(event: any) {
    const condition = this.parseTypeValue(event.value);
    this.conditionParams_2 = this.pointParams.filter(
      (item: any) => item.type === 'count' && item.en !== condition.en,
    );
  }

  typeForm = new FormGroup({
    type: new FormControl(''),
  });

  staticForm = new FormGroup({
    type: new FormControl(''),
    conditionType: new FormControl(''),
    result: new FormControl(''),
    binaryResult: new FormControl(''),
  });

  conditionForm = new FormGroup({
    type: new FormControl(''),
    arg_1: new FormControl(''),
    arg_2: new FormControl(''),
    resultType: new FormControl(''),
    result: new FormControl(''),
  });

  constructor(
    private staticService: StaticService,
    private taskService: TaskService,
  ) {}

  ngOnInit(): void {
    this.staticService.getPointColumns().subscribe((res: any) => {
      this.pointParams = res.map((item: any) => {
        let type = '';

        const name = item.ru.toLowerCase();

        if (name.includes('?')) {
          type = 'binary';
          // } else if (name.includes('дата выдачи')) {
          //   type = 'date';
        } else if (name.includes('дата')) {
          type = 'count-date';
        } else if (name.includes('количество')) {
          type = 'count';
        }
        return {
          ...item,
          type,
        };
      });
      this.conditionParams_1 = this.pointParams.filter(
        (item: any) => item.type === 'count',
      );
      this.conditionParams_2 = this.conditionParams_1;

      this.taskService.getTaskConditionsOperatorsAll().subscribe((res: any) => {
        // console.log('Виды выражений: ', res.items);
        this.allConditionTypes = res.items;
        this.conditionTypes = res.items.filter(
          (item: any) =>
            item.name.includes('сложение') ||
            item.name.includes('вычитание') ||
            item.name.includes('умножение') ||
            item.name.includes('деление'),
        );
        this.conditionResultTypes = res.items.filter((item: any) => {
          return (
            (item.name.includes('больше') ||
              item.name.includes('меньше') ||
              item.name.includes('равно')) &&
            item.name.includes('n_дней') === false
          );
        });
        // console.log('Тип результата для выражений: ', this.conditionResultTypes);
        // console.log('Тип результата для параметров: ', this.pointConditionTypes);
        this.check();
      });
    });
  }

  getTypeValue(type: any) {
    return JSON.stringify(type);
  }

  parseTypeValue(type: string): any {
    return JSON.parse(type);
  }

  onPointParamChange(event: any) {
    this.selectedParam = event.value;

    const selectedType = this.parseTypeValue(this.selectedParam);

    this.pointConditionType = selectedType.type;

    const hasCondition = selectedType.type === 'binary' ? false : true;

    if (hasCondition) {
      this.updatePointConditionTypes(selectedType);
    }
  }

  updatePointConditionTypes(type: any) {
    this.pointConditionTypes = [];

    if (type.type === 'count-date') {
      this.pointConditionTypes = this.allConditionTypes.filter(
        (item: any) => item.tag == 'Даты',
      );
    } else {
      this.pointConditionTypes = this.allConditionTypes.filter(
        (item: any) => item.tag == 'Логические',
      );
    }
  }

  @Output() onSubconditionAdd = new EventEmitter();

  addSubCondition() {
    let formulaItem = {
      key: '',
      value: <any>{},
      type: this.selectedType,
    };

    if (this.selectedType === 'static') {
      let { type, binaryResult, conditionType, result } = this.staticForm.value;

      const selectedParam = this.parseTypeValue(<string>type);

      formulaItem.key = selectedParam.en;

      if (selectedParam.type === 'binary') {
        formulaItem.value = binaryResult === 'true' ? true : false;
      } else {
        const condition = this.parseTypeValue(<string>conditionType);
        formulaItem.value[condition.name] =
          selectedParam.type !== 'date'
            ? parseInt(<string>result)
            : new Date(<any>result).toISOString();
      }
    } else if (this.selectedType === 'condition') {
      const formData = this.conditionForm.value;

      const conditionType = this.parseTypeValue(<any>formData.type);
      const arg_1 = this.parseTypeValue(<any>formData.arg_1);
      const arg_2 = this.parseTypeValue(<any>formData.arg_2);
      const resultType = this.parseTypeValue(<any>formData.resultType);
      const value = parseFloat(<any>formData.result);

      formulaItem.key = conditionType.name;
      formulaItem.value = {
        $арг1: arg_1.en,
        $арг2: arg_2.en,
      };
      formulaItem.value[resultType.name] = value;
    }

    const isChanging = this.isAdded;

    this.onSubconditionAdd.emit({ index: this.index, formulaItem, isChanging });
  }

  check() {
    if (this.subcondition.type) {
      this.typeForm.setValue({ type: this.subcondition.type });

      this.selectedType = this.subcondition.type;

      if (this.selectedType === 'static') {
        let staticForm: any = {
          type: '',
          binaryResult: '',
          conditionType: '',
          result: '',
        };

        const param = this.pointParams.filter(
          (item: any) => item.en === this.subcondition.key,
        )[0];

        this.selectedParam = this.getTypeValue(param);
        this.pointConditionType = param.type;

        staticForm.type = this.selectedParam;

        if (param.type == 'binary') {
          staticForm.binaryResult = String(this.subcondition.value);
        } else {
          this.updatePointConditionTypes(param);

          const type = Object.keys(this.subcondition.value)[0];
          const conditionType = this.getTypeValue(
            this.allConditionTypes.filter((item: any) => item.name === type)[0],
          );
          const conditionResult = this.subcondition.value[type];

          staticForm.conditionType = conditionType;
          staticForm.result = conditionResult;
        }

        this.staticForm.setValue(staticForm);
      } else {
        console.log(this.subcondition);

        let form: any = {
          type: '',
          arg_1: '',
          arg_2: '',
          resultType: '',
          result: '',
        };

        form.type = this.getTypeValue(
          this.allConditionTypes.filter(
            (item: any) => item.name === this.subcondition.key,
          )[0],
        );

        const value = this.subcondition.value;

        form.arg_1 = this.getTypeValue(
          this.pointParams.filter(
            (items: any) => items.en === value['$арг1'],
          )[0],
        );
        form.arg_2 = this.getTypeValue(
          this.pointParams.filter(
            (items: any) => items.en === value['$арг2'],
          )[0],
        );

        let resultType = Object.keys(value).filter(
          (key: string) => key != '$арг1' && key != '$арг2',
        )[0];

        form.result = value[resultType];

        resultType = this.allConditionTypes.filter(
          (item: any) => item.name === resultType,
        )[0];
        resultType = this.getTypeValue(resultType);

        form.resultType = resultType;

        this.conditionForm.setValue(form);
      }
    }
  }

  onTypeChange(event: any) {
    const value = event.value;
    this.selectedType = value;
  }
}
