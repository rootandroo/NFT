<template>
  <div class="row asset-modal q-pr-md q-pb-md bg-dark">
    <div class="col-6 col-grow q-pt-md q-pl-md">
      <q-card class="q-px-sm shadow-6">
        <span class="text-h6 text-weight-bold text-dark">{{ 'Rarity Rank #' + asset.rank }}</span>
        <q-img 
          :src="src" 
          loading="lazy"
          no-spinner
          img-class="rounded-borders"
        >
          <template #loading>
            <q-skeleton
              class="fit"
              square
            />
          </template>
        </q-img>
        <q-card-section class="text-body1 text-dark text-weight-bold ellipsis">
          <span class="row justify-center">{{ label }}</span>
          <div class="row justify-center">
            <q-btn
              v-if="price"
              class="rounded-borders bg-positive q-pa-sm q-mt-sm title"
              @click="open(asset.market?.CNFTio.id)"
            >
              <q-avatar
                size="sm"
                class="q-mr-sm"
                square
              >
                <img src="../assets/cnft.png">
              </q-avatar>
              <div class="q-px-sm text-positive rounded-borders bg-white text-h6 text-weight-bolder self-center">
                <span>{{ price }} ADA</span>
              </div>
            </q-btn>
          </div>
        </q-card-section>
      </q-card>
    </div>
    <div 
      v-if="collection.included_keys"
      class="col-grow q-pt-md q-pl-md" 
    >
      <div class="rounded-borders bg-positive title q-pa-sm">
        <span class="text-h5 text-dark text-weight-bold">
          Rarity Score
        </span>
        <q-badge
          color="white"
          class="q-mt-sm row justify-center "
        >
          <span class="text-h6 text-positive text-weight-bold">
            {{ asset.score }}
          </span>
        </q-badge>
      </div>
      
      <div class="wrapper q-mt-sm">
        <q-scroll-area class="fit">
          <q-card
            v-for="key in Object.keys(collection.included_keys)"
            :key="key"
            class="q-mb-xs rounded-borders text-dark"
          >
            <q-card-section class="q-px-sm q-pb-sm q-pt-none">
              <span class="text-body1">{{ getLabel(key) }}</span>
              <q-list
                class="q-ma-xs"
              >
                <dist-checkbox 
                  v-if="!collection.included_keys[key]"               
                  :trait="key"
                  :option="getOption(key)"
                  :count="collection.distribution[key][getOption(key)]"
                  :tag-obj="values[key][getOption(key)]"
                  :is-active="isActive(key, getOption(key))"
                />  
    
                <!-- Option is Array -->
                <dist-checkbox 
                  v-for="elm in getOption(key)"
                  v-else
                  :key="elm"
                  :trait="key"
                  :option="elm"
                  :count="collection.distribution[key][elm]"
                  :tag-obj="values[key][elm]"
                  :is-active="isActive(key, elm)"
                />
              </q-list>
            </q-card-section>
          </q-card>
        </q-scroll-area>
      </div>
    </div>
  </div>
</template>

<script>
import DistCheckbox from './DistCheckbox.vue'
import { mapState, mapGetters } from 'vuex'
import { openURL } from 'quasar'

export default {
  components: {
    DistCheckbox
  },

  // eslint-disable-next-line vue/require-prop-types
  props: ['src', 'asset', 'label', 'price'],

  computed: {
    ...mapState('api', [
      'collection',
      'values'
    ]),
  
    ...mapGetters('api', [
      'isActive',
    ]),

    getLabel() {
      return string => {
        return string.split('_').at(-1)
      }
    },

    getOption() {
      return key => {
        return this.asset.onchain_metadata[key] ? this.asset.onchain_metadata[key] : 'null'
      }
    }
  },

  methods: {
    open (id) {
      openURL("https://cnft.io/token/" + id)
    }
  }
}
</script>

<style lang="scss" scoped>
.asset-modal {
  width: 100%;
  height: 90%;
  max-width: 700px;
  overflow: auto;
  &::-webkit-scrollbar {
    display: none;
  }
}

.q-badge {
  width: 100%;
}

.title {
  text-align: center;
}

.wrapper {
  height: calc(100% - 100px);
  min-height: 300px;
}

.q-item {
  background-color: white;
  padding-left: 8px !important;
  padding-right: 8px !important;
}

.q-item.active {
  background-color: #74eda5 !important;
}
</style>>