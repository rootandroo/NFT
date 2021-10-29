<template>
  <q-item-section>
    <q-input
      v-model="serialInput"
      label="Lookup By Serial"
      label-color="white"
      dense
      type="number"
      dark
      debounce="500"
      @update:model-value="handleSerialUpdate"
    />
  </q-item-section>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";
export default {
  computed: {
    ...mapState("api", ["serial"]),

    serialInput: {
      get() {
        return this.serial;
      },
      set(val) {
        this.updateSerial(val);
      },
    },
  },

  methods: {
    ...mapMutations("api", ["updateSerial"]),

    ...mapActions("api", ["fetchAssets"]),

    handleSerialUpdate() {
      this.fetchAssets();
    },
  },
};
</script>

<style>

input[type="number"]::-webkit-outer-spin-button, input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
 
input[type="number"] {
    -moz-appearance: textfield;
}
</style>