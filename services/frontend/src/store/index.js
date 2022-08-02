import createPersistedState from "vuex-persistedstate";
import { createStore } from 'vuex'

import notes from './modules/notes';
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
    notes,
    users,
    cars,
  },
  plugins: [createPersistedState()],
})
