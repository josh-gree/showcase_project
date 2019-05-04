import Vue from 'vue'
import App from './App.vue'
import VueNativeSock from 'vue-native-websocket'

const host = document.location.host
const uri = "ws://" + host + "/ws"
Vue.use(VueNativeSock, uri, { reconnection: true, format: 'json' })
// const uri = "ws://localhost:5678"
// Vue.use(VueNativeSock, uri, { reconnection: true, format: 'json' })

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
