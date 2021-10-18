import axios from "axios"


const state = () => ({
  urls: {},
  headers: {'Authorization':''},
  policyID: null,
  serial: null
})


const getters = {
}


const actions = {
  fetchProjects ({ commit, state }) {
    axios
      .get(state.urls.list_project, { headers: state.headers })
      .then(response => {
        var projectList = response.data.results.map(project => project.name)
        commit('updateProjectList', projectList, {root:true})
      })
  },

  fetchPolicies ({ commit, state }, project) {
    const config = {
          headers: state.headers,
          params: { project:project }
    }
    axios
      .get(state.urls.list_collection, config)
      .then(response => {
        var policyList = response.data.results.map(collection => collection.policy_id)
        commit('updatePolicyList', policyList, {root:true})
              
        // Set Selected policyID
        if (policyList.length == 1) {
          commit('updatePolicyID', policyList[0])
        }
      })
  },

  fetchDistribution({ commit, state }, policyID) {
    const config = { headers: state.headers }
    axios
      .get(state.urls.list_collection + policyID, config)
      .then(response => {
        var distribution = response.data.distribution
        commit('updateDistribution', distribution, {root:true})
      })
  },

  async fetchAssets ({ commit, state }, {policyID, url=null, serial=null, tags=null}) {
    var append = url === null ? false : true 
    url = url || state.urls.list_asset
    const config = {
      headers: state.headers,
      params: {
        policy_id: policyID,          
        serial: serial,
        query_obj: tags
      }
    }
    const resp = await axios.get(url, config)
    var payload = {
      list: resp.data.results,
      append: append
    }
    commit('updateAssetList', payload, {root:true})
    return (resp.data.next)
  }
}


const mutations = {
  setApi (state, urls) {
    state.urls = {...state.urls, ...urls}
  },

  setAuth (state, token) {
      state.headers.Authorization = 'Token'.concat(' ',token)
  },

  updatePolicyID (state, policyID) {
    state.policyID = policyID
  },

  updateSerial (state, serial) {
    state.serial = serial
  }
} 


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}