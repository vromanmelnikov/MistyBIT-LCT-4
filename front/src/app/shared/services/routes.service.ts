import { P } from "@angular/cdk/keycodes";
import { Injectable } from "@angular/core";
import { NavigationEnd, Router } from "@angular/router";

@Injectable()
class RoutesService {

    constructor(private router: Router) { }

    routes: any = {
        '/manager/points': 'Управление точками',
        '/manager/profile': 'Профиль менеджера',
        '/manager/employeers': 'Управление сотрудниками',
        '/employee/profile': 'Личный кабинет сотрудника',
        '/employee/tasks': 'Мои задачи',
        '/employee/constructor': 'Конструктор задач',
        '/auth/login': 'Авторизация',
        '/not_found': 'Упс! Страница не найдена...'
    }

    routerSubscribe() {

        // this.router.events.subscribe(
        //     (value) => {

        //         if (value instanceof NavigationEnd) {

        //             const url = value.url

        //             console.log(url)

        //             // if (url === '/') {
        //             //     this.router.navigate(['/employee/profile'])
        //             // }

        //             let title = this.routes[url]
        //             if (!title) {
        //                 // title = this.routes['/not_found']
        //             }

        //             window.document.title = title

        //         }

        //     }
        // )

    }

}
export default RoutesService