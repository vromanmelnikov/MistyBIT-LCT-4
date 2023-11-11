import { Employeer, Manager } from '../models/employers.model';

export default class EmployeersManagmentService {
  public employeers: Employeer[] = [
    {
      id: 0,
      lastname: 'Иванов',
      firstname: 'Иван',
      patronymic: 'Иванович',
      email: 'ivanov@mail.ru',
      office: {
        id: -1,
        address: '',
      },
      grade: {
        id: -1,
        name: '',
      },
    },
    {
      id: 2,
      lastname: 'Горячев',
      firstname: 'Георгий',
      patronymic: 'Самсонович',
      email: 'goryachev@mail.ru',
      office: {
        id: -1,
        address: '',
      },
      grade: {
        id: -1,
        name: '',
      },
    },
  ];
  public managers: Manager[] = [
    {
      id: 1,
      lastname: 'Денисов',
      firstname: 'Денис',
      patronymic: 'Денисович',
      email: 'denisov@mail.ru',
    },
    {
      id: 1,
      lastname: 'Денисов',
      firstname: 'Денис',
      patronymic: 'Денисович',
      email: 'denisov@mail.ru',
    },
    {
      id: 1,
      lastname: 'Денисов',
      firstname: 'Денис',
      patronymic: 'Денисович',
      email: 'denisov@mail.ru',
    },
    {
      id: 1,
      lastname: 'Денисов',
      firstname: 'Денис',
      patronymic: 'Денисович',
      email: 'denisov@mail.ru',
    },
    {
      id: 1,
      lastname: 'Денисов',
      firstname: 'Денис',
      patronymic: 'Денисович',
      email: 'denisov@mail.ru',
    },
  ];

  public employeersDisplayedColumns: any[] = [
    {
      key: 'lastname',
      viewValue: 'Фамилия',
    },
    {
      key: 'firstname',
      viewValue: 'Имя',
    },
    {
      key: 'patronymic',
      viewValue: 'Отчество',
    },
    {
      key: 'email',
      viewValue: 'Почта',
    },
    {
      key: 'grade',
      viewValue: 'Почта',
    },
    {
      key: 'office',
      viewValue: 'Почта',
    },
  ];

  public managersDisplayedColumns: any[] = [
    {
      key: 'lastname',
      viewValue: 'Фамилия',
    },
    {
      key: 'firstname',
      viewValue: 'Имя',
    },
    {
      key: 'patronymic',
      viewValue: 'Отчество',
    },
    {
      key: 'email',
      viewValue: 'Почта',
    },
  ];

  constructor() {}
}
