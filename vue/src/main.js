import '@babel/polyfill'
import 'mutationobserver-shim'
import './plugins/bootstrap-vue'
import App from './App.vue'
import Vue from 'vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
