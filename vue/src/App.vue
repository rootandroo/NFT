<template>
  <div id="wrapper" class="h-100 p-0">
    <sidebar/>
    <div id="content" class="bg-light-accent">
      <navbar/>
      <assets/>
    </div>
  </div>
</template>

<script>
import navbar from './components/navbar.vue'
import sidebar from './components/sidebar.vue'
import assets from './components/assets.vue'

export default {
  name: 'App',
  components: {
    navbar,
    sidebar,
    assets
  },
}
</script>

<style lang="scss">
@import "~@/assets/scss/vendors/bootstrap-vue/index";
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#wrapper {
  display: flex;
  width: 100%;
  align-items: flex-start;
}

.b-container {
  padding: 0px;
}

#content {
  width: 100%;
  height: 100%;
}
</style>
