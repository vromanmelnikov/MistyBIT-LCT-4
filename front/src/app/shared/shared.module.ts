import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DATE_LOCALE } from '@angular/material/core';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatDialogModule } from '@angular/material/dialog';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { HttpClientModule } from '@angular/common/http';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatRadioModule } from '@angular/material/radio';
// import { FormFieldComponent } from './components/form-field/form-field.component';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSelectModule } from '@angular/material/select';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSliderModule } from '@angular/material/slider';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatChipsModule } from '@angular/material/chips';
// import { OptionComponent } from './components/option/option.component';
import { MatBadgeModule } from '@angular/material/badge';
import { MatStepperModule } from '@angular/material/stepper';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { FormFieldComponent } from './components/form-field/form-field.component';
import { AngularYandexMapsModule, YaConfig } from 'angular8-yandex-maps';
import { environment } from 'src/environments/environment';
import { YandexMapComponent } from './components/yandex-map/yandex-map.component';
import { ProfileComponent } from './components/profile/profile.component';
import { SkillsComponent } from './components/profile/skills/skills.component';
import { GradeComponent } from './components/profile/skills/grade/grade.component';
import { PhotoComponent } from './components/profile/photo/photo.component';
import { InfoComponent } from './components/profile/info/info.component';
import { CurrentTaskComponent } from './components/current-task/current-task.component';
import { FeedbackDialogComponent } from './components/feedback-dialog/feedback-dialog.component';
import { RecoverPasswordDialogComponent } from './components/profile/info/recover-password-dialog/recover-password-dialog.component';
import { GroupByPipe } from './pipes/notsGroupByDate.pipe';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { NotificationsComponent } from './components/notifications/notifications.component';
@NgModule({
  imports: [

    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatSnackBarModule,
    MatButtonModule,
    MatCardModule,
    MatDividerModule,
    MatIconModule,
    MatToolbarModule,
    MatDialogModule,
    MatCheckboxModule,
    MatRadioModule,
    MatAutocompleteModule,
    MatMenuModule,
    MatFormFieldModule,
    MatSidenavModule,
    MatSelectModule,
    MatExpansionModule,
    MatSliderModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatBadgeModule,
    MatStepperModule,
    MatTableModule,
    MatSortModule,
    AngularYandexMapsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatSlideToggleModule
    // MatSnackBarModule,
  ],
  exports: [
    MatNativeDateModule,
    MatDatepickerModule,
    GroupByPipe,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
    MatSnackBarModule,
    MatCardModule,
    MatDividerModule,
    MatToolbarModule,
    MatDialogModule,
    MatCheckboxModule,
    MatRadioModule,
    MatAutocompleteModule,
    MatMenuModule,
    MatSidenavModule,
    MatSelectModule,
    MatExpansionModule,
    MatSliderModule,
    MatProgressSpinnerModule,
    // MatSnackBarModule,
    MatChipsModule,
    MatBadgeModule,
    MatStepperModule,
    MatTableModule,
    MatSortModule,
    FormFieldComponent,
    YandexMapComponent,
    ProfileComponent,
    MatSlideToggleModule,
    NotificationsComponent,
    // SkillsComponent,
    // GradeComponent,
    // PhotoComponent,
    // InfoComponent
    // .forRoot(mapConfig)
  ],
  declarations: [
    GroupByPipe,
    FormFieldComponent,
    YandexMapComponent,
    ProfileComponent,
    SkillsComponent,
    GradeComponent,
    PhotoComponent,
    InfoComponent,
    CurrentTaskComponent,
    FeedbackDialogComponent,
    RecoverPasswordDialogComponent,
    NotificationsComponent,

  ],
  providers: [{ provide: MAT_DATE_LOCALE, useValue: 'ru-RU' }],
})
export class SharedModule {}
