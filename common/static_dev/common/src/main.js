import {createApp} from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import formatLib from "./formatLib.js";
import ToastPlugin from 'vue-toast-notification';

String.prototype.toTitleCase = function () {
  return this.trim().split(' ').map(w =>
    w[0].toUpperCase() + w.substring(1).toLowerCase()).join(' ');
};


const app = createApp(App);
app.use(router);
app.use(store);
app.use(ToastPlugin, {
  position: 'top',
  duration: 1000,
});
app.mount("#app");
app.config.globalProperties.$filters = formatLib;

import('vue-toast-notification/dist/theme-bootstrap.css');
