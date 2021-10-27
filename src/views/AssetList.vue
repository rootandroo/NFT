<template>
  <q-page v-if="policyID">
    <q-scroll-area
      ref="scrollArea"
      :thumb-style="{
        background:'white',
        opacity: 1,
        width: '6px',
        right: '4px'}"
    >
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
          >
            <asset-card :asset="asset" />
          </q-intersection>
        </div>
      </q-infinite-scroll>
    </q-scroll-area>
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
          this.updateTags([]) // Clear Selected Tags
          this.resetScrollArea()
          this.fetchAssets({policyID: newPolicy}).then(resp => {
            this.updateCirculation(resp.found)
          })
          this.fetchDistribution(newPolicy) 
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
        'updateCirculation'
      ]),

      onLoad (index, done) {
        if (this.nextURL) {
          this.fetchAssets({url: this.nextURL})
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

.q-scrollarea {
    height: calc(100vh - 50px);
}

.q-intersection {
  min-height: 285px;
}
</style>

