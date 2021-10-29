<template>
  <q-item-section>
    <div style="max-width: 268px">
      <q-select
        v-model="policyID"
        label="Select Drop"
        label-color="white"
        options-dense
        options-selected-class="text-white"
        dark
        :options="policyList"
        @update:model-val="updatePolicyID(policyID)"
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
        policyList: {
            type: Array,
            required: true
        }
    },

    computed: {
      ...mapState('api', [
        'policyID',
      ]),
    },

    methods: {
        ...mapMutations('api', [
          'updatePolicyID',
        ]),
    }
}
</script>

<style>

</style>