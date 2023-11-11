import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-back-is-fall',
  templateUrl: './back-is-fall.component.html',
  styleUrls: ['./back-is-fall.component.scss']
})
export class BackIsFallComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    alert('Бекенд решил умереть...')
  }

}
