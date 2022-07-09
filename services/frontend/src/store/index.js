import createPersistedState from "vuex-persistedstate";
import { createStore } from 'vuex'

import notes from './modules/notes';
import users from './modules/users';

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
  },
  plugins: [createPersistedState()],
})
