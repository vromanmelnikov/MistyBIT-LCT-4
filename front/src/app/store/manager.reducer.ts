
import { createReducer, on } from '@ngrx/store';
import { SetStaticUserInfo, setUser, setUserSkills } from './user.actions';
import { User } from '../shared/models/user.model';
import { setEmployyes } from './manager.actions';
import { Employee } from '../shared/models/employers.model';

const initialState = {
  employeers: [],
  managers: []
};

export const ManagerReducer = createReducer(
  initialState,
  on(setEmployyes, (state, action: any) => {
    const payload = action.payload
    state.employeers = payload
    return state
  })
);
