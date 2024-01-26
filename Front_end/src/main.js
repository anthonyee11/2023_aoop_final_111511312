import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import PulseLoader from 'vue-spinner/src/PulseLoader.vue'



const app = createApp(App);
app.use(VueAxios, axios);
app.component('PulseLoader', PulseLoader)


app.mount('#app');