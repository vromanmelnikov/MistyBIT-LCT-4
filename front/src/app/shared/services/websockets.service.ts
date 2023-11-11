// import { ProfileService } from 'src/app/shared/services/profile.service';
import { AuthService } from './auth.service';
import { EventEmitter, Injectable, Output } from '@angular/core';
// import { BACKEND_URL_RESOURCE_WEBSOCKET } from '../urls';
import { WebSocketSubject, webSocket } from 'rxjs/webSocket';
import { InputMessage } from '../models/message.model';
import { environment } from 'src/environments/environment';
import { showMessage } from '../common';
import { MatSnackBar } from '@angular/material/snack-bar';

const TIMEOUT = 5000;
@Injectable({
  providedIn: 'root',
})
export class WebSocketService {
  @Output() MessageGetted = new EventEmitter<any>();

  ws: WebSocketSubject<unknown> | undefined;
  SendMessage(message: InputMessage) {
    this.ws?.next(message);
  }

  Close() {
    this.ws?.complete();
  }

  constructor(private authService: AuthService, private snackbar: MatSnackBar) {}

  Connect() {

    const token = this.authService.GetAccessToken()

    this.ws = webSocket(`${environment.NOTIF_URL}/ws?client_key=1&token=${token}`,)
    this.ws?.asObservable().subscribe(
      (dataFromServer: any) => {
        if (!dataFromServer.code) {
          this.MessageGetted.emit(dataFromServer);
        }        
      },
      (err) => {
        setTimeout(() => {
          this.Connect();
        }, TIMEOUT);
      },
      () => {},
    );
  }
}
