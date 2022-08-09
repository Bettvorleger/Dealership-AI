import { createApp } from 'vue'
import axios from 'axios';
import App from './App.vue'
import router from './router'
import store from './store'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'

// set fastapi URL for axios for CORS exception
const loc = document.location;
axios.defaults.withCredentials = true;
axios.defaults.baseURL = loc.protocol + '//' + loc.hostname + '/fastapi';  // the FastAPI backend

// auto logout user after 30 minutes
axios.interceptors.response.use(undefined, function (error) {
    if (error) {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            store.dispatch('logOut');
            return router.push({ name: 'login' })
        }
    }
});

createApp(App).use(Quasar, quasarUserOptions).use(router).use(store).mount('#app')
