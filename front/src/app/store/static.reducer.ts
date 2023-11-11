import { createReducer, on } from '@ngrx/store';
import { SetAllSkillsAction, SetOfficesAction, SetPointsAction } from './static.actions';

const initialState = {
  allSkills: [],
  offices: [],
  points: []
};

export const StaticReducer = createReducer(
  initialState,
  on(SetAllSkillsAction, (state, action: any) => {
    const payload = action.payload;
    state.allSkills = payload;
    return state;
  }),
  on(SetOfficesAction, (state, action: any) => {
    const payload = action.payload;
    state.offices = payload;
    return state;
  }),
  on(SetPointsAction, (state, action: any) => {
    const payload = action.payload;
    state.points = payload;
    return state;
  })
);
