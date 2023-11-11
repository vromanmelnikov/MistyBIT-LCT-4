interface Coordinates {
    lat: number,
    lon: number
}

type FieldType = string | number

interface Field {
    value: FieldType,
}

interface PointsParams {
    id: 0,
    address: ''
    coordinate: Coordinates,
    field_links: Field[]
}


export class Point{
    constructor(
        public id: number,
        public address: string,
        public img: string,
        public is_delivered_card: boolean,
        public is_delivered_card_conv: string,
        public created_at: string,
        public created_at_conv: string,
        public last_date_issue_card: string,
        public last_date_issue_card_conv: string,
        public quantity_card: number,
        public quantity_requests: number
    ) {}
}