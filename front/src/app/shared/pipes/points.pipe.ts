import { Pipe, PipeTransform } from '@angular/core';
import { Employee } from '../models/employers.model';
import { Point } from '../models/points.model';

@Pipe({
  name: 'employee',
})
export class PointsPipe implements PipeTransform {
  transform(points: any, ...args: any[]) {
    let res = points.map((value: any): Point => {

      const is_delivered_card_conv = value.is_delivered_card ? 'Да' : 'Нет'

      let last_date_issue_card_conv = ''
      if (value.last_date_issue_card) {
        last_date_issue_card_conv = value.last_date_issue_card.split('T')[0]
      }
      else {
        last_date_issue_card_conv = '-'
      }

      const created_at_conv = value.created_at.split('T')[0]

      const item: Point = {
        id: value.id,
        address: value.address,
        img: value.img,
        is_delivered_card: value.is_delivered_card,
        is_delivered_card_conv,
        created_at: value.created_at,
        created_at_conv,
        last_date_issue_card: value.last_date_issue_card,
        last_date_issue_card_conv,
        quantity_card: value.quantity_card,
        quantity_requests: value.quantity_requests
      };
      return item;
    });
    return res;
  }
}
