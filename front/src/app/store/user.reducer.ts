import { createReducer, on } from '@ngrx/store';
import { SetStaticUserInfo, setUser, setUserSkills } from './user.actions';
import { User } from '../shared/models/user.model';

const initialState = {
  profile: {
    lastname: 'Иванов',
    firstname: 'Иван',
    patronymic: 'Иванович',
    email: 'ivanov@mail.ru',
    id: -1,
    img: '',
    role: {
      id: -1,
      name: 'Менеджер',
      is_public: false,
    },
  },
  skills: [],
  office: {
    id: -1,
    address: ''
  },
  grade: {
    id: -1,
    name: ''
  }
};

export const userReducer = createReducer(
  initialState,
  on(setUser, (state, action: any) => {
    const payload = action.payload;


    state.profile = structuredClone(payload);
    console.log(payload)
    return state;
  }),
  on(setUserSkills, (state, action: any) => {
    const payload = action.payload;
    state.skills = structuredClone(payload);
    return state;
  }),
  on(SetStaticUserInfo, (state, action: any) => {
    state.office = action.office;
    state.grade = action.grade;
    return state;
  }),
);
