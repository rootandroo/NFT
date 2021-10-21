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
          class="card-group q-pa-lg q-gutter-lg"
          :v-if="assetList"
        >
          <q-intersection
            v-for="asset in assetList"
            :key="asset.name"
          >
            <q-card 
              class="q-px-sm shadow-6"
              @click="asset.modal = true"
            >
              <span class="text-h6 text-dark">{{ '#' + asset.rank }}</span>
              <q-img 
                :src="fetchImagePath(asset.onchain_metadata.image)" 
                loading="lazy"
                spinner-color="dark"
                class="asset-img"
              />

              <q-card-section class="asset-name text-dark">
                <span class="text-body2">{{ getAssetLabel(asset) }}</span>
              </q-card-section>
              <q-dialog v-model="asset.modal">
                <asset-modal-content
                  :src="fetchImagePath(asset.onchain_metadata.image)"
                  :asset="asset"
                  :label="getAssetLabel(asset)"
                />
              </q-dialog>
            </q-card>
          </q-intersection>
        </div>
      </q-infinite-scroll>
    </q-scroll-area>
  </q-page>
</template>

<script>
import AssetModalContent from '../components/AssetModalContent.vue'
import { mapActions, mapState, mapMutations } from 'vuex'

export default {
  components: { AssetModalContent },
  
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
      getAssetLabel ()  {
          return asset => asset.onchain_metadata.title ?? asset.onchain_metadata.name
      }
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

      fetchImagePath: function (ipfs) {
          var ipfs_id = /[^/]*$/.exec(ipfs)[0];
          return 'https://ipfs.blockfrost.dev/ipfs/' + ipfs_id
      },

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
	grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
}

.q-scrollarea {
    height: calc(100vh - 50px);
}

.q-intersection {
  min-height: 351px;
}

.asset-name {
  text-align: center;
}

.asset-img {
  border-radius: 4px !important;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19) !important;
  min-height: 263px;
}
</style>

