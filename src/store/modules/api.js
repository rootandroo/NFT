import axios from "axios"


const state = () => ({
  urls: {},
  headers: {'Authorization':''},
  collection: null,
  serial: null, // Unecessary after Asset Modal is Linked with Vue Router
  nextURL: null, // Next Page URL
  tags: [], // Filter by {attribute:option}
  values: {}, // storing Tag Objects for reference
  rankFilter: {"min": null, "max": null}, // Filter by min and max rank
  priceFilter: {"min": null, "max": null}, // Filter by min and max price
  circulation: 0
})


const getters = {
  isActive: (state, getters) => (trait, option) => {
    var tag = getters.createTag(trait, option)
    var tags = JSON.parse(JSON.stringify(state.tags))
    return tags.some(e => JSON.stringify(e[trait]) == JSON.stringify(tag[trait]))
  },

  isTraitSelected: (state, getters) => (trait) => {
    var values = JSON.parse(JSON.stringify(Object.values(state.values[trait])))
    return values.some(e => getters.isActive(trait, e[trait]))
  },

  createValues: (state, getters) => (distribution) => {
    var result = {}
    for (const [trait, obj] of Object.entries(distribution)) {
      result[trait] = {}
      for (const option of Object.keys(obj)) {
        result[trait][option] = getters.createTag(trait, option)
      }
    }
    return result
  },

  createTag: (state, getters) => (trait, option) => {
    return state.collection.included_keys[trait] ? {[trait]:new Array(option)} : {[trait]:option}
  },

  calcPercentage: (state) => (count) => {
    return ((count/state.circulation) * 100).toFixed(3) + '%'
  }
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

  async fetchCollections ({ commit, state }, project) {
    const config = {
          headers: state.headers,
          params: { project:project }
    }
    const resp = await axios.get(state.urls.list_collection, config)
    var collectionList = resp.data.results
    commit('updateCollectionList', collectionList, {root:true})      
    return collectionList        
  },

  async fetchAssets ({ commit, state }, append=false) {
    var url = append ? state.nextURL : state.urls.list_asset
    
    const config = {
      headers: state.headers,
      params: {
        policy_id: state.collection.policy_id,          
        query_obj: JSON.stringify(state.tags),
        rank_filter: state.rankFilter,
        price_filter: state.priceFilter,
        serial: state.serial,
      }
    }

    try {
      const resp = await axios.get(url, config)
      var payload = { list: resp.data.results, append: append }
      commit('updateAssetList', payload, {root:true})
      commit('updateNextURL', resp.data.next)
      return {found:resp.data.count}
    } catch (error) {
      commit('updateNextURL', null)
      return {found: 0}
    }
  }
}


const mutations = {
  setApi (state, urls) {
    state.urls = {...state.urls, ...urls}
  },

  setAuth (state, token) {
      state.headers.Authorization = 'Token'.concat(' ',token)
  },

  updateCollection (state, collection) {
    state.collection = {...state.collection, ...collection}
  },

  updateSerial (state, serial) {
    state.serial = serial
  },

  updateTags (state, tags) {
    state.tags = tags
  },

  updateValues (state, obj) {
    state.values = obj
  },

  updateNextURL (state, url) {
    state.nextURL = url
  },
  
  updateCirculation (state, count) {
    state.circulation = count
  },

  updateRankFilter (state, {min, max}) {
    state.rankFilter["min"] = min
    state.rankFilter["max"] = max
  },

  updatePriceFilter (state, {min, max}) {
    state.priceFilter["min"] = min
    state.priceFilter["max"] = max
  }
} 


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}