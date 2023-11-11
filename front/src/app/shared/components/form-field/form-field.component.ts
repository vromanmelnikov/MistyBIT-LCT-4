import {
  Component,
  ElementRef,
  forwardRef,
  Input,
  OnInit,
  ViewChild,
} from '@angular/core';
import {
  AbstractControl,
  ControlValueAccessor,
  NG_VALUE_ACCESSOR,
} from '@angular/forms';

@Component({
  selector: 'app-form-field',
  templateUrl: './form-field.component.html',
  styleUrls: ['./form-field.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      multi: true,
      useExisting: forwardRef(() => FormFieldComponent),
    },
  ],
})
export class FormFieldComponent implements OnInit, ControlValueAccessor {
  @Input()
  formConrol: AbstractControl | null | undefined | any;
  @Input()
  label: any = '';
  @Input()
  placeholder = '';
  @Input()
  type: string = '';
  @Input()
  icon: any = '';
  @Input()
  messageErorFunc: any = () => {};
  @Input()
  colorBorder: any = null;
  @Input()
  borderRadius: any = '50px';
  @Input()
  disable: boolean = false;
  @Input()
  date_cls: string = 'date-input';

  getClass() {
    return this.type == 'date' ? this.date_cls : '';
  }

  style() {
    if (this.colorBorder)
      return {
        'border-radius': this.borderRadius,
        border: `1px solid ${this.colorBorder}`,
      };
    else return { 'border-radius': this.borderRadius };
  }

  onClick() {
    if (this.type === 'date') {
      let inp: any = document.getElementsByClassName(this.date_cls)[0];
      if (inp) {
        inp.showPicker();
      }
    }
  }
  _value = '';
  get value() {
    return this._value;
  }
  @Input()
  set value(val: string) {
    this._value = val;
    this.onChange(this._value);
  }
  onChange: any = () => {};
  onTouched: any = () => {};
  constructor() {}
  ngOnInit(): void {}
  writeValue(value: string): void {
    console.log(value);
    this.value = value;
  }
  registerOnChange(fn: any): void {
    console.log(fn);
    this.onChange = fn;
  }
  registerOnTouched(fn: any): void {
    console.log(fn);
    this.onTouched = fn;
  }
  onInput(e: any) {
    this.value = e.target.value;
  }
}
