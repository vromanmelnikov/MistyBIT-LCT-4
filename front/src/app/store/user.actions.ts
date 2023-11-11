import { createAction, Action } from '@ngrx/store';
import { Grade, Office, User } from '../shared/models/user.model';
import { Skill } from '../shared/models/employers.model';

export const setUser = createAction('[User] Set user', (payload: User) => {
  return { payload };
});

export const setUserSkills = createAction(
  '[User] Set user`s skills',
  (payload: Skill[]) => ({ payload }),
);

export const SetStaticUserInfo = createAction(
  '[User] Set office and grade',
  (office: Office, grade: Grade) => ({ office, grade }),
);
