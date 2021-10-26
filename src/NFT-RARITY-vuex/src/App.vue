<template>
  <q-layout
    view="lHh LpR fFf"
    class="bg-accent"
  >
    <!-- Navbar -->
    <q-header 
      class="bg-primary text-white"
      height-hint="50"
    >
      <q-toolbar>
        <q-btn
          dense
          flat
          round
          icon="menu"
          @click="toggleSidebar"
        />
        <q-toolbar-title>
          <!-- <q-img
            id="logo"
            src="./assets/logo.png"
          /> -->
        </q-toolbar-title>

        <links />
      </q-toolbar>
    </q-header>

    <!-- Sidebar -->
    <q-drawer
      v-model="sidebar"
      class="bg-dark"
      show-if-above
      side="left"
      :width="300"
      :breakpoint="500"
    >
      <sidebar-content />
    </q-drawer>

    <!-- Content -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import SidebarContent from './components/SidebarContent.vue'
import Links from './components/Links.vue'
import { mapMutations, mapActions } from 'vuex'
const URLS = JSON.parse(document.getElementById('json_data').textContent).urls

export default {
  name: 'App',

  components: {
    SidebarContent,
    Links
  },

  data () {
    return {
      sidebar: false,
    }
  },

  mounted () {
    this.setApi(URLS)
    this.setAuth(process.env.VUE_APP_TOKEN)
    this.fetchProjects()
  },

  methods: {
    toggleSidebar () {
      this.sidebar = !this.sidebar
    },

    ...mapMutations('api', [
      'setApi',
      'setAuth'
    ]),

    ...mapActions('api', [
      'fetchProjects'
    ])
  },
}
</script>

<style lang="scss" scoped>
  #logo {
    width: 150px;
  }
</style>