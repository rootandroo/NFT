<template>
  <q-page v-if="policyID">
    <q-infinite-scroll 
      :offset="250"
      :debounce="700"
      @load="onLoad"
    >
      <div
        class="card-group q-pa-lg q-gutter-md"
        :v-if="assetList"
      >
        <q-intersection
          v-for="asset in assetList"
          :key="asset.name"
          transition="fade"
        >
          <asset-card :asset="asset" />
        </q-intersection>
      </div>
    </q-infinite-scroll>
  </q-page>
</template>

<script>
import AssetCard from '../components/AssetCard.vue'
import { mapActions, mapState, mapMutations } from 'vuex'

export default {
  components: { 
    AssetCard
  },
  
  data () {
      return {
          nextPage: null
      }
  },

  computed: {
      ...mapState('api', [
          'policyID',
          'nextURL'
      ]),

      ...mapState([
          'assetList'
      ]),
  },

  watch: {
      '$route.params.project' (project) {
          this.fetchPolicies(project)
      },
      policyID (newPolicy, oldPolicy) {
          console.log(`Updating from ${oldPolicy} to ${newPolicy}`)
           
          //  Reset Filters
          this.updateTags([]) 
          this.updatePriceFilter({min:null, max:null})
          this.updateRankFilter({min:null, max:null})

          this.resetScrollArea()
          this.fetchAssets().then(resp => {
            this.updateCirculation(resp.found)
          })
          this.fetchDistribution() 
      }
  },

  created () {
      this.fetchPolicies(this.$route.params.project)
  },

  methods: {
      ...mapActions('api', [
          'fetchPolicies',
          'fetchAssets',
          'fetchDistribution'
      ]),

      ...mapMutations('api', [
        'updateTags',
        'updateCirculation',
        "updatePriceFilter",
        "updateRankFilter"
      ]),

      onLoad (index, done) {
        if (this.nextURL) {
          this.fetchAssets({append:true})
        }
        done()
      },

      resetScrollArea () {
        if (this.$refs.scrollArea) {
          this.$refs.scrollArea.setScrollPosition('vertical', 0) 
        }
      }
  }    
}
</script>

<style>
.card-group {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
}

.q-intersection {
  min-height: 285px;
}
</style>

