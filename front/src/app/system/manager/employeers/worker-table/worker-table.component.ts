import { Component, Input, OnInit } from '@angular/core';
import { Employeer, Manager } from 'src/app/shared/models/employers.model';
import { animate, state, style, transition, trigger } from '@angular/animations';

@Component({
  selector: 'app-worker-table',
  templateUrl: './worker-table.component.html',
  styleUrls: ['./worker-table.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class WorkerTableComponent implements OnInit {

  @Input() displayedColumns: any[] = []

  columns: string[] = this.displayedColumns.map(column => column.key)

  @Input() list: Manager[] | Employeer[] = [];
  filteredList: Manager[] | Employeer[] = []

  expandedElement: Manager | Employeer | null = null;

  constructor() { }

  ngOnInit(): void {

    this.filteredList = [...this.list]

    console.log(this.displayedColumns)
    console.log(this.list)

  }

  clickElement(element: Manager) {
    this.expandedElement = this.expandedElement === element ? null : element
  }

  applyFilter(event: Event) {

    const filterValue = (event.target as HTMLInputElement).value.toLowerCase();

    if (filterValue === '') {
      this.filteredList = [...this.list]
    }
    else {

      this.filteredList = this.list.filter(item => {

        const lastname = item.lastname.toLowerCase()
        const firstname = item.firstname.toLowerCase()
        const patronymic = item.patronymic.toLowerCase()
        const email = item.email.toLowerCase()

        if (
          lastname.includes(filterValue) ||
          firstname.includes(filterValue) ||
          patronymic.includes(filterValue) ||
          email.includes(filterValue)
        ) {
          return true
        }
        else {
          return false
        }

      })

    }

  }

}
