import { Injectable } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";

@Injectable()
export default class ComponentsService {

    constructor(private _snackBar: MatSnackBar){

    }

    openSnackbar(message: string, action: string = 'Хорошо') {
        console.log(message)
        // this._snackBar.open(message, action, {
        //     horizontalPosition: 'center',
        //     verticalPosition: 'top'
        // })
    }

}