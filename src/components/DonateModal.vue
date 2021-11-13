<template>
  <q-btn
    no-caps
    class="full-width"
    label="Donate"
    text-color="dark"
    color="white"
    @click="donate = true"
  />
  <q-dialog v-model="donate">
    <q-card
      class="bg-dark"
      style="width: 700px; max-width: 80vw;"
    >
      <q-card-section class="text-white">
        <q-input
          v-model="adaAddress" 
          readonly
          dark
          outlined
          dense
        />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
    name: 'DonateModal',

    data () {
        return {
            donate: false,
            adaAddress: `addr1qxufz8nu0s6my5rvqns3xjsupfcua4uw4l5p0jc69hlp8de92xc8xqrc9xlv798vg95y47p2w243e3lwj8vnd8f2rlrsy8fs04`,
        }
    }
}
</script>

<style>
</style>