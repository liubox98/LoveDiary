import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from './plugins/axios';

import Vant from 'vant';
import 'vant/lib/index.css';

const app = createApp(App);
app.config.globalProperties.$axios = axios;

app.use(router);
app.use(store);
app.use(Vant);
app.mount('#app');
