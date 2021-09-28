<template>
  <div id="wrapper" class="h-100 p-0">
    <the-sidebar/>
    <div id="content" class="bg-light-accent">
      <the-navbar/>
      <the-asset-list/>
    </div>
  </div>
</template>

<script>
import TheNavbar from './components/TheNavbar.vue'
import TheSidebar from './components/TheSidebar.vue'
import TheAssetList from './components/TheAssetList.vue'

export default {
  name: 'App',
  components: {
    TheNavbar,
    TheSidebar,
    TheAssetList,
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
