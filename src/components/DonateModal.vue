<template>
  <q-btn
    no-caps
    class="full-width"
    label="Donate"
    text-color="dark"
    color="positive"
    @click="donate = true"
  />
  <q-dialog v-model="donate">
    <q-card class="bg-dark">
      <q-card-section class="text-white">
        {{ message }}<br>
        {{ adaAddress }}
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
            adaAddress: `addr1qxufz8nu0s6my5rvqns3xjsupfcua4uw4l5p0jc69hlp
                         8de92xc8xqrc9xlv798vg95y47p2w243e3lwj8vnd8f2rlrsy8fs04`,
            message: `I am a student developer based in New York, and 
                      recently developed an interest in CNFTs. I created NFT RARITY 
                      to aid in determining rarity and consequent value of NFTs.`
        }
    }
}
</script>

<style>
</style>