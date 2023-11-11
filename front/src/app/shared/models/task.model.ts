export class TypeTaskPostModel {
  constructor(
    public name: any,
    public priority_id: any,
    public duration: any,
    public details: any,
    public interval_block: any,
  ) {}
}

export class TypeTaskPutModel {
  constructor(
    public id: any,
    public name: any,
    public priority_id: any,
    public duration: any,
    public details: any,
    public interval_block: any,
  ) {}
}

export class TypeTaskGradePostModel {
  constructor(
    public type_task_id: any,
    public grade_id: any,
  ) {}
}

export class TypeTaskSkillPostModel {
  constructor(
    public type_task_id: any,
    public skill_id: any,
  ) {}
}

export class ConditionPostModel {
  constructor(
    public description: any,
    public formula: any,
    public task_id: any,
  ) {}
}


