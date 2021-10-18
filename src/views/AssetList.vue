<template>
  <q-page>
    <q-scroll-area
      :thumb-style="{
        background:'white',
        opacity: 1,
        width: '6px',
        right: '4px'}"
    >
      <q-infinite-scroll>
        <div
          class="card-group q-pa-md q-gutter-md"
          :v-if="assetList"
        >
          <q-intersection
            v-for="asset in assetList"
            :key="asset.name"
          >
            <q-card>
              <q-img 
                :src="fetchImagePath(asset.onchain_metadata.image)" 
                loading="lazy"
                spinner-color="dark"
              />

              <q-card-section>
                {{ getAssetLabel(asset) }}
              </q-card-section>
            </q-card>
          </q-intersection>
        </div>
      </q-infinite-scroll>
    </q-scroll-area>
  </q-page>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
    data () {
        return {
            nextPage: ''
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
            this.fetchAssets({policyID: newPolicy}).then(url => {this.nextPage = url}) // Fetch assets and set nextPage
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

        fetchImagePath: function (ipfs) {
            var ipfs_id = /[^/]*$/.exec(ipfs)[0];
            return 'https://ipfs.blockfrost.dev/ipfs/' + ipfs_id
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
</style>

