import { HttpClient } from '@angular/common/http';
import { Injectable, Output, EventEmitter } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { environment } from 'src/environments/environment';
import { HttpErrorResponse } from '@angular/common/http';
import {
  ConditionPostModel,
  TypeTaskGradePostModel,
  TypeTaskPostModel,
  TypeTaskPutModel,
  TypeTaskSkillPostModel,
} from '../models/task.model';

@Injectable()
export default class TaskService {
  TASKS_URL = `${environment.API_URL}/tasks`;
  constructor(private http: HttpClient) {}
  @Output()
  ReloadTask = new EventEmitter<any>();

  getTasksAll(
    limit?: number,
    offset?: number,
    type_id?: number,
    point_id?: number,
    status_id?: number,
    priority_id?: number,
    employee_id?: number,
    date_create?: any,
    date_begin?: any,
    to_all?: boolean,
  ) {
    let params: any = {};

    if (limit) {
      params.limit = limit;
    }
    if (offset) {
      params.offset = offset;
    }
    if (type_id) {
      params.type_id = type_id;
    }
    if (point_id) {
      params.point_id = point_id;
    }
    if (status_id) {
      params.status_id = status_id;
    }
    if (priority_id) {
      params.priority_id = priority_id;
    }
    if (employee_id) {
      params.employee_id = employee_id;
    }
    if (date_create) {
      params.date_create = date_create;
    }
    if (date_begin) {
      params.date_begin = date_begin;
    }
    if (to_all !== undefined) {
      params.to_all = to_all;
    }

    return this.http
      .get(`${this.TASKS_URL}/`, {
        params: { ...params },
      })
      .pipe(
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }),
      );
  }
  getTasksHistoryAll(limit?: number, offset?: number, employee_id?: number) {
    let params: any = {};

    if (limit) {
      params.limit = limit;
    }
    if (offset) {
      params.offset = offset;
    }
    if (employee_id) {
      params.employee_id = employee_id;
    }
    return this.http
      .get(`${this.TASKS_URL}/history`, {
        params: { ...params },
      })
      .pipe(
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }),
      );
  }
  getTaskConditionsOperatorsAll() {
    return this.http.get(`${this.TASKS_URL}/conditions/operators/all`).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  getStatusesAll(in_history?: boolean) {
    let params: any = {};
    if (in_history != undefined) {
      params.in_history = in_history;
    }
    return this.http
      .get(`${this.TASKS_URL}/statuses/all`, {
        params: { ...params },
      })
      .pipe(
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }),
      );
  }
  getPrioritiesAll() {
    return this.http.get(`${this.TASKS_URL}/priorities/all`).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  getTasksTypes() {
    return this.http.get(`${this.TASKS_URL}/types`).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  addTaskType(task_type: TypeTaskPostModel) {
    return this.http.post(`${this.TASKS_URL}/types`, task_type).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  changeTaskType(task_type: TypeTaskPutModel) {
    return this.http.put(`${this.TASKS_URL}/types`, task_type).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  deleteTaskType(id: number) {
    return this.http.delete(`${this.TASKS_URL}/types?id=${id}`).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  addTaskTypeGrade(type_task: TypeTaskGradePostModel) {
    return this.http.post(`${this.TASKS_URL}/types/grades`, type_task).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  deleteTaskTypeGrade(type_task: TypeTaskGradePostModel) {
    const httpOptions = {
      body: type_task,
    };
    return this.http.delete(`${this.TASKS_URL}/types/grades`, httpOptions).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  addTaskTypeSkill(type_task: TypeTaskSkillPostModel) {
    return this.http.post(`${this.TASKS_URL}/types/skills`, type_task).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  deleteTaskTypeSkill(type_task: TypeTaskSkillPostModel) {
    const httpOptions = {
      body: type_task,
    };
    return this.http.delete(`${this.TASKS_URL}/types/skills`, httpOptions).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  addTaskCondition(cond: ConditionPostModel) {
    return this.http.post(`${this.TASKS_URL}/conditions`, cond).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  deleteTaskCondition(id: number) {
    return this.http
      .delete(`${this.TASKS_URL}/conditions?condition_id=${id}`)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }),
      );
  }
  putTaskCondition(cond: ConditionPostModel) {
    return this.http.put(`${this.TASKS_URL}/conditions`, cond).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  addTaskDefine() {
    return this.http.post(`${this.TASKS_URL}/define`, '').pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }
  addTaskDistribution(begin_hour?: number, end_hour?: number) {
    let params: any = {};
    if (begin_hour) {
      params.begin_hour = begin_hour;
    }
    if (end_hour) {
      params.end_hour = end_hour;
    }
    return this.http
      .post(`${this.TASKS_URL}/distribution`, { params: { ...params } })
      .pipe(
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }),
      );
  }

  taskCancelled(id: number, feedback_description?: any) {
    return this.http
      .post(`${this.TASKS_URL}/cancelled?id=${id}`, {
        id: id,
        feedback_description: feedback_description,
      })
      .pipe(
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }),
      );
  }
  taskAccept(id: number) {
    let params: any = {};
    params.id = id;

    return this.http
      .put(`${this.TASKS_URL}/accept_task?task_id=${id}`, '')
      .pipe(
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }),
      );
  }

  taskCompleted(id: number, feedback_value?: any, feedback_description?: any) {
    return this.http
      .post(`${this.TASKS_URL}/completed`, {
        id: id,
        feedback_value: feedback_value,
        feedback_description: feedback_description,
      })
      .pipe(
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }),
      );
  }
  taskDelete() {
    return this.http.delete(`${this.TASKS_URL}/tasks`).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      }),
    );
  }

  getReport() {
    return this.http.get<Blob>(`${this.TASKS_URL}/report`, {
      observe: 'response',
      responseType: 'blob' as 'json',
    });
  }
}
