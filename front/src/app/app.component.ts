import { Component, OnInit } from '@angular/core';
import RoutesService from './shared/services/routes.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {

  title = 'front';

  constructor(private routesService: RoutesService, private router: Router) {
    routesService.routerSubscribe()
  }

  ngOnInit() {


    // this.router.navigate(['/employee/profile'])

  }

}
