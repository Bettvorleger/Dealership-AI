import { createApp } from 'vue'
import axios from 'axios';
import App from './App.vue'
import router from './router'
import store from './store'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5001/';  // the FastAPI backend

createApp(App).use(Quasar, quasarUserOptions).use(router).use(store).mount('#app')
