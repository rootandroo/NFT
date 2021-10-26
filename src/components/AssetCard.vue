<template>
  <q-card 
    class="q-px-sm shadow-6"
    @click="modal = true"
  >
    <div class="text-body1 text-weight-bold text-dark">
      {{ '#' + asset.rank }}
      <!-- <span
        v-if="price"
        class="text-positive text-h6 float-right"
      >{{ formatToAda(price) }}</span>
      <q-skeleton
        v-else-if="price === null"
        type="QBadge"
        class="float-right q-mt-sm"
      /> -->
    </div>
    <q-img 
      :src="fetchImagePath(asset.onchain_metadata.image)" 
      loading="lazy"
      no-spinner
      class="asset-img"
    >
      <template #loading>
        <q-skeleton
          class="fit"
          square
        />
      </template>
    </q-img>
    <q-card-section class="asset-name text-dark">
      <span class="text-body2">{{ getAssetLabel(asset) }}</span>
    </q-card-section>
    <q-dialog v-model="modal">
      <asset-modal-content
        :src="fetchImagePath(asset.onchain_metadata.image)"
        :asset="asset"
        :label="getAssetLabel(asset)"
      />
    </q-dialog>
  </q-card>
</template>

<script>
import AssetModalContent from '../components/AssetModalContent.vue'
// import axios from 'axios'

export default {

  components: { 
      AssetModalContent,
  },

  props: {
      asset: {
          type: Object,
          required: true
      },
  },
  
  data () {
      return {
          modal: this.asset.modal,
          price: null,
          id: undefined
      } 
  },

  computed: {
      getAssetLabel ()  {
          return asset => asset.onchain_metadata.title ?? asset.onchain_metadata.name
      },

      // formatToAda () {
      //   return lovelace => lovelace / 1_000_000 + " ADA"
      // }
  },

  // created () {
  //   this.fetchAssetMarketInfo(this.asset.onchain_metadata.name)
  // },

  methods: {
      fetchImagePath (ipfs) {
          var ipfs_id = /[^/]*$/.exec(ipfs)[0];
          return 'https://ipfs.blockfrost.dev/ipfs/' + ipfs_id
      },

      // fetchAssetMarketInfo (name) {
      //     const params = new URLSearchParams()
      //     params.append("search", name);
      //     params.append("sort", "date");
      //     params.append("order", "desc");
      //     params.append("page", 1);
      //     axios
      //       .post('https://api.cnft.io/market/listings', params)
      //       .then(resp => {
      //           this.price = resp.data.assets[0]?.price
      //           this.id = resp.data.assets[0]?.id
      //       })
      // }
  }
}
</script>

<style lang="scss" scoped>
.asset-name {
  text-align: center;
}

.asset-img {
  border-radius: 4px !important;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19) !important;
  min-height: 182px;
}
</style>