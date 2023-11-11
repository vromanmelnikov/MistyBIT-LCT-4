import { StoreModule } from '@ngrx/store';
import { userReducer } from './user.reducer';
import { StaticReducer } from './static.reducer';
import { ManagerReducer } from './manager.reducer';

const RootStoreModule = StoreModule.forRoot({
  user: userReducer,
  static: StaticReducer,
  manager: ManagerReducer,
}, {
  runtimeChecks: {
    strictStateImmutability: false,
    strictActionImmutability: false,
  },
});

export default RootStoreModule;
