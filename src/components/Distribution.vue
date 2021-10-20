<template>
  <q-item-section>
    <q-item-label class="text-white text-h6">
      Distribution
    </q-item-label>
    <q-list
      dark
      class="rounded-borders"
    >
      <q-expansion-item
        v-for="[trait, obj] in Object.entries(distribution)"
        :key="trait"
        dense
        :label="getLabel(trait)"
        header-class="text-body1"
      >
        <q-list
          class="q-py-sm q-px-md"
          dense
        >
          <q-item
            v-for="[option, count] in Object.entries(obj)"
            :key="option"
            v-ripple
            tag="label"
            :class="[activeClass(trait, option), 'bg-white', 'rounded-borders', 'q-mb-xs']"
          >
            <dist-checkbox 
              :trait="trait"
              :option="option"
              :count="count"
              :tag-obj="tagObject(trait, option)"
              :active="activeClass(trait, option)"
            />
          </q-item>
        </q-list>
      </q-expansion-item>
    </q-list>
  </q-item-section>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import DistCheckbox from './DistCheckbox.vue'

export default {
  
  components: {
    DistCheckbox
  },

  computed: {
    ...mapState([
      'distribution',
      'includedKeys'
    ]),

    ...mapState('api', [
      'tags'
    ]),

    ...mapGetters('api', [
      'activeClass',
      'tagObject'
    ]),

    getLabel() {
      return string => {
        return string.substring(string.lastIndexOf('_') + 1);
      }
    },
  }
}
</script>


<style lang="scss" scoped>
  .title {
      color: white;
      margin-top: 5px;
      margin-bottom: 0px;
  }

  .q-item {
    padding-left: 8px !important;
    padding-right: 8px !important;
  }

  .q-item.active {
    background-color: #74eda5 !important;
  }
</style>