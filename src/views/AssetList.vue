<template>
  <q-page v-if="policyID">
    <q-scroll-area
      :thumb-style="{
        background:'white',
        opacity: 1,
        width: '6px',
        right: '4px'}"
    >
      <q-infinite-scroll 
        :offset="250"
        :debounce="700"
        transition="fade"
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
          'policyID'
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
          this.updateTags([])
          this.fetchAssets({policyID: newPolicy}).then(resp => {
            this.nextPage = resp.next
            this.updateCirculation(resp.count)
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
        if (this.nextPage) {
          this.fetchAssets({url: this.nextPage}).then(resp => {this.nextPage = resp.next})
        }
        done()
      },
  }    
}
</script>

<style>
.card-group {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(13rem, auto));
}

.q-scrollarea {
    height: calc(100vh - 50px);
}

.q-intersection {
  min-height: 285px;
}
</style>

