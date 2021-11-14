<template>
  <q-item-section>
    <div style="max-width: 268px">
      <q-select
        v-model="collectionInput"
        label="Select Drop"
        label-color="white"
        options-dense
        options-selected-class="text-white"
        dark
        :options="collectionList"
        option-label="name"
      >
        <template #selected-item="scope">
          <div class="ellipsis">
            {{ scope.opt }}
          </div>
        </template>
      </q-select>
    </div>
  </q-item-section>
</template>

<script>
import { mapMutations, mapState } from 'vuex'
export default {
    props: {
        collectionList: {
            type: Array,
            required: true
        }
    },

    computed: {
      ...mapState('api', [
        'collection',
      ]),

      collectionInput: {
        get() { return this.collection?.name },
        set(collection) {
          this.updateCollection(collection)
        }
      }
    },

    methods: {
        ...mapMutations('api', [
          'updateCollection',
        ]),
    }
}
</script>

<style>

</style>