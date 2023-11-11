import { createAction, Action } from '@ngrx/store';
import { Employee } from '../shared/models/employers.model';

export const setEmployyes = createAction('[Manager] Set employees', (payload: Employee[]) => {
  console.log(payload)
  return { payload };
});
