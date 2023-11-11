import { Observable } from "rxjs";

export type SelectInput = {
    field: string;
    type: any;
    label: string;
    formControl: any;
    messageError?: () => string;
    values?: Observable<any[]>;
    placeholder?: any;
    icon?: string;
    onClick?: (p:any) => void;
    hide?: boolean;
  };
  