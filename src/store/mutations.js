export default {
    updateProjectList (state, list) {
      state.projectList = list
    },

    updatePolicyList (state, list) {
      state.policyList = list
    },

    updateAssetList (state, {append, list}) {
      list.forEach(asset => asset['modal'] = false);
      if (append) {
        state.assetList.push(...list)
      } else {
        state.assetList = list
      }
    },

    updateDistribution (state, distribution) {
      state.distribution = distribution
    },

    updateKeys (state, keys) {
      state.includedKeys = keys
    },
}