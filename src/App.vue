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
          icon="search"
          @click="toggleSidebar"
        />
        <a
          href="/"
          class="text-white text-h6"
        >
          NFT RARITY
        </a>
        <links />
      </q-toolbar>
    </q-header>

    <!-- Sidebar -->
    <q-drawer
      v-model="sidebar"
      show-if-above
      class="bg-dark"
      side="left"
      :width="300"
    >
      <sidebar-content />
    </q-drawer>

    <!-- Content -->
    <q-page-container>
      <q-scroll-area
        ref="scrollArea"
        :thumb-style="{
          background:'white',
          opacity: 1,
          width: '6px',
          right: '4px'}"
      >
        <router-view />
      </q-scroll-area>
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

  .q-scrollarea {
    height: calc(100vh - 50px);
  }

  a:link {
    text-decoration: none;
  }
</style>