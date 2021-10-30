<template>
  <q-form
    class="row q-gutter-md items-center"
    @submit="onSubmit"
  >
    <q-input
      v-model="min"
      class="col-3"
      label="min"
      label-color="white"
      dense
      dark
      type="number"
      hint="PRICE"
    />
    <q-input
      v-model="max"
      class="col-3"
      label="max"
      label-color="white"
      dense
      dark
      type="number"
      hint=""
    />
    <div>
      <q-btn
        type="submit"
        class="col-3"
        color="white"
        text-color="black"
        label="Apply"
        size="sm"
      />
    </div>
  </q-form>        
</template>

<script>
import { mapMutations, mapActions } from 'vuex'
export default {
  data () {
      return {
        min: null,
        max: null,
      }
  },
  methods: {
    ...mapMutations("api", ["updatePriceFilter"]),

    ...mapActions("api", ["fetchAssets"]),

    onSubmit () {
      var min = this.min ? parseInt(this.min) : null 
      var max = this.max ? parseInt(this.max) : null
      this.updatePriceFilter({min, max})
      this.fetchAssets()
    }
  }
}
</script>

<style>

</style>