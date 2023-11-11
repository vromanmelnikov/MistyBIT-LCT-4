import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Store } from '@ngrx/store';
import TaskService from 'src/app/shared/services/task.service';

@Component({
  selector: 'app-archieve-list-task',
  templateUrl: './archieve-list-task.component.html',
  styleUrls: ['./archieve-list-task.component.css']
})
export class ArchieveListTaskComponent implements OnInit {

  @Input() flag: boolean = false
  @Output() onChange = new EventEmitter()
  list: any
  employee_id: any;
  constructor(private taskService: TaskService, private store: Store<any>,) { }

  ngOnInit(): void {
    this.store.subscribe((res) => {
      this.employee_id = res.user.profile.id;
      this.taskService.getTasksHistoryAll(undefined, undefined, this.employee_id).subscribe(
        (res: any) => {
          this.list = res.items
          console.log(this.list)
        }
      )
      this.taskService.getStatusesAll(true).subscribe(
        (res: any) => {
          this.allStatuses = res.items
          console.log(this.allStatuses)
        }
      )
    })
    
  }

  showList(item: any) {

    console.log(item)

  }

  clickBackdrop(event: any) {

    console.log(event.target)

    if (event.target.id === 'close-target') {
      
      this.onChange.emit(false)

    }

  }

  createFullStar(mark: number){
    return Array.from(Array(mark));
  }
  createStar(mark: number){
    return Array.from(Array(5 - mark));
  }
  allStatuses: any
  getStatusTask(status_id: number){
    const status = this.allStatuses.filter(function(item: any) {return item.id==status_id})
    return status[0].name
    // return this.allStatuses.find(function(item: any) {return item.id==status_id})
  }

}
