import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { FeedbackDialogComponent } from '../feedback-dialog/feedback-dialog.component';
import TaskService from 'src/app/shared/services/task.service';
import { Store } from '@ngrx/store';
import { StepperSelectionEvent } from '@angular/cdk/stepper';
import { showMessage } from 'src/app/shared/common';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatStepper } from '@angular/material/stepper';
import { ErorrDialogComponent } from '../error-dialog/error-dialog.component';

const ACCEPTED_TASK_ID = 4;
const FAILED_ACCEPTED_TASK = 'Не удалось принять задачу';
const FAILED_COMPLETE_TASK = 'Не удалось отметить задачу как выполненную';
const FAILED_CANCEL_TASK = 'Не удалось отменить задачу';

@Component({
  selector: 'app-current-task',
  templateUrl: './current-task.component.html',
  styleUrls: ['./current-task.component.css'],
})
export class CurrentTaskComponent implements OnInit {
  label_go = 'Выезд';
  label_finish = 'Завершение';
  currentIndex = 0;
  current: any;
  employee_id: any;
  isCompleted = true;

  @ViewChild('stepper', { static: false })
  stepperComponent: MatStepper | undefined;

  constructor(
    private dialog: MatDialog,
    private taskService: TaskService,
    private _snackBar: MatSnackBar,
    private store: Store<any>,
  ) {}

  loadTasks() {
    this.store.subscribe((res) => {
      this.employee_id = res.user.profile.id;
      this.taskService
        .getTasksAll(
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
          this.employee_id,
          undefined,
          undefined,
          false,
        )
        .subscribe(
          (res: any) => {
            this.current = res.items[0];

            if (this.current.status_id == ACCEPTED_TASK_ID) {
              this.currentIndex = 1;
            }
          },
          (err) => {
            this.current = null;
          },
        );
    });
  }

  ngOnInit(): void {
    this.loadTasks();

    this.taskService.ReloadTask.subscribe(() => {
      this.loadTasks();
      this.resetSteper();
    });
  }

  selectionChange(event: StepperSelectionEvent) {
    if (event.previouslySelectedIndex < event.selectedIndex) {
      if (event.selectedStep.label == this.label_finish) {
        this.acceptTask();
      }
    }
  }

  resetSteper() {
    if (this.stepperComponent) {
      this.stepperComponent.reset();
    }
  }

  cancelTast() {
    const dialogRef = this.dialog.open(ErorrDialogComponent, {
      data: {},
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.taskService
          .taskCancelled(this.current.id, result.description)
          .subscribe(
            (res: any) => {
              this.taskService.ReloadTask.emit();
              this.resetSteper();
              showMessage(this._snackBar, res.message);
            },
            (err) => {
              console.log(err);
              showMessage(this._snackBar, FAILED_CANCEL_TASK);
            },
          );
      }
    });
  }

  finishTask() {
    const dialogRef = this.dialog.open(FeedbackDialogComponent, {
      data: {},
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.taskService
          .taskCompleted(this.current.id, result.stars, result.description)
          .subscribe(
            (res: any) => {
              this.taskService.ReloadTask.emit();
              this.resetSteper();
              showMessage(this._snackBar, res.message);
            },
            (err) => {
              console.log(err);
              showMessage(this._snackBar, FAILED_COMPLETE_TASK);
            },
          );
      }
    });
  }
  acceptTask() {
    this.taskService.taskAccept(this.current.id).subscribe(
      (res: any) => {
        showMessage(this._snackBar, res.message);
      },
      (err) => {
        console.log(err);
        showMessage(this._snackBar, FAILED_ACCEPTED_TASK);
      },
    );
  }

  goToYaMaps() {
    const button: any = document.getElementsByClassName(
      'ymaps-2-1-79-gotoymaps__container',
    )[0];
    button.click();
  }
}
