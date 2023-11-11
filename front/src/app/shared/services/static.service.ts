import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable()
export default class StaticService {
  constructor(private http: HttpClient) { }
  OFFICE_URL = environment.API_URL + '/offices'
  getAllSkills() {
    return this.http.get(environment.API_URL + '/skills/all').pipe(
      //@ts-ignore
      catchError((error: any) => {
        if (error.status === 404) return throwError([]);
      }),
    );
  }

  getAllOffices() {
    return this.http.get(environment.API_URL + '/offices/all').pipe(
      //@ts-ignore
      catchError((error: any) => {
        if (error.status === 404) return throwError([]);
      }),
    );
  }

  deleteOffice(id: number) {
    return this.http.delete(environment.API_URL + '/offices/', { params: { id } });
  }

  getAllGrades() {
    return this.http.get(environment.API_URL + '/users/grades/all').pipe(
      //@ts-ignore
      catchError((error: any) => {
        if (error.status === 404) return throwError([]);
      }),
    );
  }

  getAllPoints() {
    return this.http.get(environment.API_URL + '/offices/points/').pipe(
      //@ts-ignore
      catchError((error: any) => {
        if (error.status === 404) return throwError([]);
      }),
    );
  }

  addOffice(address: string) {
    return this.http.post(environment.API_URL + '/offices/', { address });
  }

  addPoint(address: string) {
    return this.http.post(environment.API_URL + '/offices/points', { address });
  }

  countWeights(flag: boolean) {
    return this.http.get(environment.API_URL + '/offices/count_weights', {params: {count_remains: flag}})
  }

  deletePoint(id: number) {
    return this.http.delete(environment.API_URL + '/offices/points', { params: { id } });
  }

  getAllRoles() {
    return this.http.get(environment.API_URL + '/users/roles/all').pipe(
      //@ts-ignore
      catchError((error: any) => {
        if (error.status === 404) return throwError([]);
      }),
    );
  }

  changeOfficeAddress(id: number, address: string) {
    return this.http.put(environment.API_URL + '/offices', { id, address })
  }
  putPoint(id: number, address: any, coordinate?: any) {
    return this.http.put(`${this.OFFICE_URL}/points`, { id: id, address: address, coordinate: coordinate },
    ).pipe(catchError((error: HttpErrorResponse) => { return throwError(error) }))
  }
  putPointIsDeliveredCard(id: number) {
    return this.http.put(`${this.OFFICE_URL}/points/is_delivered_card?id=${id}`, "",
    ).pipe(catchError((error: HttpErrorResponse) => { return throwError(error) }))
  }
  putPointQuantityRequests(id: number, number: number) {
    return this.http.put(`${this.OFFICE_URL}/points/quantity_requests?id=${id}&number=${number}`, "",
    ).pipe(catchError((error: HttpErrorResponse) => { return throwError(error) }))
  }
  putPointQuantityCard(id: number, number: number) {
    return this.http.put(`${this.OFFICE_URL}/points/quantity_card?id=${id}&number=${number}`, "",
    ).pipe(catchError((error: HttpErrorResponse) => { return throwError(error) }))
  }
  getPointColumns() {
    return this.http.get(`${this.OFFICE_URL}/points/columns`
    ).pipe(catchError((error: HttpErrorResponse) => { return throwError(error) }))
  }
}
