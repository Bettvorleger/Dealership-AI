import createPersistedState from "vuex-persistedstate";
import { createStore } from 'vuex'

import users from './modules/users';
import cars from './modules/cars';

export default createStore({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    users,
    cars,
  },
  plugins: [createPersistedState()],
})
