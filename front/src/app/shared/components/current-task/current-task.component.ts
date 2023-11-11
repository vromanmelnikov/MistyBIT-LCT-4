import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import TasksService from 'src/app/shared/services/tasks.service';
import { FeedbackDialogComponent } from '../feedback-dialog/feedback-dialog.component';

@Component({
  selector: 'app-current-task',
  templateUrl: './current-task.component.html',
  styleUrls: ['./current-task.component.css']
})
export class CurrentTaskComponent implements OnInit {

  current: any

  constructor(private tasksService: TasksService, private dialog: MatDialog) { }

  ngOnInit(): void {

    this.current = this.tasksService.employeerTasks.current

  }

  finishTask() {

    const dialogRef = this.dialog.open(FeedbackDialogComponent, {
      data: {id: this.current.id},
    });

  }

  goToYaMaps() {
    console.log('туть')
    const button = document.getElementsByClassName('ymaps-2-1-79-gotoymaps__container')[0]
    console.log(button)
  }

}
