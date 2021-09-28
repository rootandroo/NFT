import '@babel/polyfill'
import 'mutationobserver-shim'
import './plugins/bootstrap-vue'
import VueObserveVisibility from 'vue-observe-visibility'
import App from './App.vue'
import Vue from 'vue'

Vue.use(VueObserveVisibility)
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
