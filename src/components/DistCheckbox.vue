<template>
  <q-item-section :class="[active, 'text-dark']">
    {{ option }}
  </q-item-section>
  <q-item-section side>
    <q-badge :class="[active, 'bg-positive']">
      {{ count }}
    </q-badge>
    <q-checkbox
      v-model="selectedTags"
      :val="tag"
      class="hidden"
      size="xs"
    />
  </q-item-section>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

export default {
    // eslint-disable-next-line vue/require-prop-types
    props: ['trait', 'option', 'count', 'tagObj', 'active'],
     
    data () {
      return {
        tag: null
      }
    },

    computed: {
        ...mapState('api', [
            'tags',
            'policyID'
        ]),

        selectedTags: {
            get () {
                return this.tags
            },
            set (val) {
                this.updateTags(val)
                this.fetchAssets({policyID:this.policyID})
            }
        },
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
.active {
    color: white !important;
}
.q-badge.active {
    color: #8D4D72 !important;
    background-color: #F5F4F4 !important;
}
</style>
