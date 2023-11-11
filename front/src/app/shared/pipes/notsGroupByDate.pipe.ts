import { Component, Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'groupByDate'})
export class GroupByPipe implements PipeTransform {
    transform(collection: Array<any>, property: string = 'date_create'): Array<any> | null {
        if(!collection) {
            return null;
        }
        for (let i=0; i<collection.length; i++){
            collection[i]['date_copy']= collection[i]['date_create']
            collection[i]['date_create']=collection[i]['date_create'].toString().split('T').slice(0, 1).join(' ')
            console.log( collection[i]['date_create'])
        }
        const gc = collection.reduce((previous, current)=> {
            if(!previous[current[property]]) {
                previous[current[property]] = [current];
            } else {
                previous[current[property]].push(current);
            }
                
            return previous;
        }, {});
        const sortedKeys = Object.keys(gc).sort((a, b) => new Date(b).getTime() - new Date(a).getTime());

        const sortedData = sortedKeys.reduce((obj: any, key: any) => {
        obj[key] = gc[key];
        return obj;
        }, {});

        return Object.keys(sortedData).map(key => ({ key, value: sortedData[key] }));
    }
}