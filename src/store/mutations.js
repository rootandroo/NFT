export default {
    updateProjectList (state, list) {
      state.projectList = list
    },

    updatePolicyList (state, list) {
      state.policyList = list
    },

    updateAssetList (state, {append, list}) {
      if (append) {
        state.assetList.concat(list)
      } else {
        state.assetList = list
      }
    },

    updateDistribution (state, distribution) {
      state.distribution = distribution
    }
}