import { createStore } from 'vuex'
import api from './modules/api'
import actions from './actions'
import mutations from './mutations'

export default createStore({
  state: {
    projectList: [],
    policyList: [],
    assetList: [],
    distribution: null
  },

  mutations,

  actions,
  
  modules: {
    api
  }
})
