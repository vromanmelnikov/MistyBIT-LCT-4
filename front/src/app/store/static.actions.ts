import { createAction } from "@ngrx/store";
import { Skill } from "../shared/models/employers.model";
import { Office } from "../shared/models/user.model";
import { Point } from "../shared/models/points.model";
import { Role } from "../shared/models/static.model";

export const SetAllSkillsAction = createAction('[Static] Set all skills action', (payload: Skill[]) => ({payload}))
export const SetOfficesAction = createAction('[Static] Set all offices action', (payload: Office[]) => ({payload}))
export const SetPointsAction = createAction('[Static] Set all points action', (payload: Point[]) => ({payload}))