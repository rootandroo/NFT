<template>
  <q-layout
    view="lHh LpR fFf"
    class="bg-accent"
  >
    <!-- Navbar -->
    <q-header class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          dense
          flat
          round
          icon="menu"
          @click="toggleSidebar"
        />
        <q-toolbar-title>
          <q-img
            id="logo"
            src="./assets/logo.png"
          />
        </q-toolbar-title>
        <q-btn
          dense
          flat
        >
          <svg
            fill="white"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z" />
          </svg>
        </q-btn>
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
import { mapMutations, mapActions } from 'vuex'
const URLS = JSON.parse(document.getElementById('json_data').textContent).urls

export default {
  name: 'App',

  components: {
    SidebarContent
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