export default {
    updateProjectList (state, list) {
      state.projectList = list
    },

    updateCollectionList (state, list) {
      state.collectionList = list
    },

    updateAssetList (state, {append, list}) {
      list.forEach(asset => asset['modal'] = false);
      if (append) {
        state.assetList.push(...list)
      } else {
        state.assetList = list
      }
    },
}