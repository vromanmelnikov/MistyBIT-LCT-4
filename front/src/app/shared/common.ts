import { MatSnackBar } from '@angular/material/snack-bar';

const DURATION_MESSAGE = 5000;
const OK = 'ОК';

export function showMessage(snackBar: MatSnackBar, text: string) {
  snackBar.open(text, OK, {
    horizontalPosition: 'center',
    verticalPosition: 'top',
    duration: DURATION_MESSAGE,
  });
}
