<template>
    <b-navbar class="navbar-expand-lg sticky-top" variant="primary">
        <b-navbar-brand> 
            <img src="../assets/logo.png" alt="logo">
        </b-navbar-brand>
        <b-navbar-nav class="my-auto ml-auto">
            <b-button v-on:click="emitToggleSidebar" variant="light" class="mr-2">Search</b-button>
        </b-navbar-nav>
    </b-navbar>
</template>

<script>
export default {
  name: 'TheNavbar',
  methods: {
      emitToggleSidebar: function () {
          this.$root.$emit('toggle-sidebar')
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    img {
        height: 50px;
    }
</style>
