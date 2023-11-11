import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import UserService from 'src/app/shared/services/user.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-photo',
  templateUrl: './photo.component.html',
  styleUrls: ['./photo.component.css'],
})
export class PhotoComponent implements OnInit {
  image = '';

  constructor(
    private store: Store<any>,
    private userService: UserService,
  ) {}

  ngOnInit(): void {
    this.store.subscribe((res) => {
      const img = res.user.profile.img;

      if (img) {
        const URL = `url(${environment.STATIC_URL}/${img})`;
        this.image = URL;
      }
    });
  }

  chooseFile() {
    let fileInput = document.getElementById('image-input');

    fileInput?.click();
  }

  onFileChange(event: any) {
    const file = event.target.files[0];

    // console.log(file);

    const formData = new FormData();
    formData.set('file', file);

    this.userService.changeUserImage(formData).subscribe((res) => {
      const URL = `url(${environment.STATIC_URL}/${res})`;
      this.image = URL;
    });
  }
}
