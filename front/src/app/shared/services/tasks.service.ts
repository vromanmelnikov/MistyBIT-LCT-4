export interface Coordinates {
  lat: number,
  long: number
}

export default class TasksService {
  public employeerTasks = {
    current: {
      id: 0,
      name: 'Задача 2',
      address: 'ул. им. Атарбекова, д. 24',
    },
    remainsList: [
      {
        id: 0,
        name: 'Задача 0',
        address: 'ул. им. Атарбекова, д. 24',
      },
      {
        id: 0,
        name: 'Задача 1',
        address: 'ул. им. Атарбекова, д. 24',
      },
    ],
    completedList: [
      {
        id: 0,
        name: 'Задача 3',
        address: 'ул. им. Атарбекова, д. 24',
        mark: 4,
      },
      {
        id: 0,
        name: 'Задача 4',
        address: 'ул. им. Атарбекова, д. 24',
        mark: 5,
      },
    ],
  };

  public points: Coordinates[] = [
    {
      lat: 45.054767, 
      long: 39.001418,
    }
  ];

  constructor() {}
}
