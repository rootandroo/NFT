<template>
  <div class="asset-modal row justify-around q-pa-md  bg-dark">
    <q-card class="q-px-sm shadow-6 col-7">
      <span class="text-h6 text-dark">{{ 'Rarity Rank #' + asset.rank }}</span>
      <q-img 
        :src="src" 
        loading="lazy"
        spinner-color="dark"
        class="asset-img"
      />
      <q-card-section class="asset-name text-dark text-body1">
        {{ label }}
      </q-card-section>
    </q-card>

    <div 
      v-if="includedKeys"
      class="q-pl-md col-5"
    >
      <div class="rounded-borders bg-positive title q-pa-sm">
        <span class="text-h5 text-dark">
          Rarity Score
        </span>
        <q-badge
          color="white"
          class="q-mt-sm row justify-center "
        >
          <span class="text-h6 text-positive">
            {{ asset.score }}
          </span>
        </q-badge>
      </div>
      
      <div class="wrapper q-mt-sm">
        <q-scroll-area class="fit">
          <q-card
            v-for="key in Object.keys(includedKeys)"
            :key="key"
            class="q-mb-xs rounded-borders text-dark"
          >
            <q-card-section class="q-pa-sm">
              <span class="text-body1">{{ getLabel(key) }}</span>
              <q-list
                class="q-ma-xs"
                :set="option = getOption(key)"
              >
                <dist-checkbox 
                  v-if="!Array.isArray(option)"               
                  :trait="key"
                  :option="option"
                  :count="distribution[key][option]"
                  :tag-obj="values[key][option]"
                  :active="activeClass(key, option)"
                />
    
                <!-- Option is Array -->
                <dist-checkbox 
                  v-for="elm in option"
                  v-else
                  :key="elm"
                  :trait="key"
                  :option="elm"
                  :count="distribution[key][elm]"
                  :tag-obj="values[key][elm]"
                  :active="activeClass(key, elm)"
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

export default {
  components: {
    DistCheckbox
  },

  // eslint-disable-next-line vue/require-prop-types
  props: ['src', 'asset', 'label'],

  computed: {
    ...mapState([
      'includedKeys',
      'distribution'
    ]),

    ...mapState('api', [
      'values'
    ]),
  
    ...mapGetters('api', [
      'activeClass',
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
  }
}
</script>

<style lang="scss" scoped>
.asset-modal, .q-badge {
  width: 100%;
}

.title {
  text-align: center;
}

.wrapper {
  height: calc(100vh - 470px);
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