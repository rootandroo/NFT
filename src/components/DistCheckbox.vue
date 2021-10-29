<template>
  <q-item
    v-ripple
    tag="label"
    :class="[activeClass, 'bg-white', 'rounded-borders', 'shadow-3', 'q-mb-xs']"
    dense
  >
    <q-item-section :class="[activeClass, 'text-dark']">
      {{ option }}
    </q-item-section>
    <q-item-section side>
      <q-badge :class="[activeClass, 'bg-positive']">
        {{ calcPercentage(count) }}
      </q-badge>
      <q-checkbox
        v-model="selectedTags"
        :val="tag"
        class="hidden"
        size="xs"
      />
    </q-item-section>
  </q-item>
</template>

<script>
import { mapState, mapMutations, mapActions, mapGetters } from 'vuex'

export default {
    // eslint-disable-next-line vue/require-prop-types
    props: ['trait', 'option', 'count', 'tagObj', 'isActive'],
     
    data () {
      return {
        tag: null
      }
    },

    computed: {
        ...mapState('api', [
          'tags',
        ]),

        ...mapGetters('api', [
          'calcPercentage'
        ]), 

        selectedTags: {
            get () {
                return this.tags
            },
            set (val) {
                this.updateTags(val)
                this.fetchAssets()
            }
        },

        activeClass () {
          return this.isActive ? 'active' : ''
        }
    },

    created () {
      this.tag = this.tagObj 
    }, 

    methods: {
        ...mapMutations('api', [
            'updateTags'
        ]),

        ...mapActions('api', [
          'fetchAssets'
        ])
    }
}
</script>

<style lang="scss" scoped>
@import '~quasar-variables-styl';
.active {
    color: white !important;
}
.q-badge.active {
    color: $dark !important;
    background-color: #F5F4F4 !important;
}
</style>
