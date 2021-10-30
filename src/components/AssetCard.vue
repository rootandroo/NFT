<template>
  <q-card 
    class="q-px-sm shadow-6"
    @click="modal = true"
  >
    <div class="text-body1 text-weight-bold text-dark">
      {{ '#' + asset.rank }}
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
    <q-card-section class="text-dark q-pa-sm">
      <div class="row justify-center">
        <span class="text-body2  ellipsis text-weight-medium ">
          {{ getAssetLabel(asset) }}
        </span>
      </div>
      <div class="row text-positive text-weight-bold text-body2 justify-center">
        <span :class="[!asset.market?.CNFTio.price ? 'text-white' : '']">{{ toADA(asset.market?.CNFTio.price) }} ADA</span>
      </div>
    </q-card-section>
    <q-dialog v-model="modal">
      <asset-modal-content
        :src="fetchImagePath(asset.onchain_metadata.image)"
        :asset="asset"
        :label="getAssetLabel(asset)"
        :price="toADA(asset.market?.CNFTio.price)"
      />
    </q-dialog>
  </q-card>
</template>

<script>
import AssetModalContent from '../components/AssetModalContent.vue'

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
          return asset => `#${asset.serial} ${asset.alpha_name}`
      },

      toADA () {
        return price => price / 1_000_000
      }
  },

  methods: {
      fetchImagePath (ipfs) {
        var ipfs_id = /Qm[1-9A-Za-z]{44}.*/.exec(ipfs)?.[0]
        return 'https://ipfs.blockfrost.dev/ipfs/' +  ipfs_id 
      },
  }
}
</script>

<style lang="scss" scoped>
.asset-img {
  border-radius: 4px !important;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19) !important;
  min-height: 208px;
}
</style>