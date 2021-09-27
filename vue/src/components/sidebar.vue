<template>
    <div id='sidebar' :class="['bg-dark', 'sticky-top', {'active':sidebar}]">
        <b-container>
            <b-form-group class="p-3 w-100 mt-3" inline>
                <h3 class="text-light">Select Project</h3>
                <b-form-select 
                   class="mb-5 bg-light" 
                  :options="projects"
                  @change="fetchPolicies">
                  </b-form-select>
                <h3 class="text-light">Select Policy</h3>
                <b-form-select
                  v-model="policy_id"
                  class="bg-light"
                  :options="policies"
                  @change="emitFetchAssets">
                </b-form-select>
                <transition name="asset_rarity">
                <div v-if="policy_id" class="mt-5 text-center">
                    <b-button id="asset_rarity" variant="light" v-on:click="toggleAssetRarity">
                        {{asset_rarity ? 'View Rarity' : 'View Asset'}}
                    </b-button>
                </div>
                </transition>
            </b-form-group>
            <footer class="footer mb-3">
                <b-button block variant="light">Donate</b-button>
            </footer>
        </b-container>
    </div>
</template>

<script>
import axios from 'axios'
const URLS = JSON.parse(document.getElementById('json_data').textContent).urls
const headers = {'Authorization':'Token'.concat(' ', process.env.VUE_APP_TOKEN)}

export default {
  name: 'sidebar',
  methods: {
      fetchProjects: function() { 
        axios
            .get(URLS.list_project, { headers: headers })
            .then(response => {
                this.projects = response.data.results.map(
                    project => project.name)
            })
      },
      fetchPolicies: function(event) {
          axios
            .get(URLS.list_collection, 
                { params: { project: event, fields: 'policy_id'} },
                { headers:headers })
            .then(response => {
                this.policies = response.data.results.map(
                    collection => collection.policy_id)
            })
      },
      // if currently viewing assets emit event to assets component
      emitFetchAssets: function() {
          this.$root.$emit('fetch-assets', this.policy_id)
      },
      emitFetchRarity: function() {
          this.$root.$emit('fetch-rarity', this.policy_id)
      },
      // return rarity distribution
      fetchDistribution: function() {
          axios
            .get(URLS.list_collection + this.policy_id, {headers:headers})
            .then(response => {
                console.log(response.data.distribution)
            })
      },
      toggleAssetRarity: function() {
          this.asset_rarity = !this.asset_rarity
      },
  },
  data () {
      return {
          projects: null,
          policies: null,
          sidebar: true,
          policy_id: '',
          asset_rarity: true
      }
  },
  created () {
      this.fetchProjects()
      this.$root.$on('toggle-sidebar', () => {
          this.sidebar = !this.sidebar
      });
  },
  beforeDestroy() {
    // removing $root listener
    this.$root.$off('toggle')
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #sidebar {
        min-width: 300px;
        max-width: 300px;
        height: 100%;
        transition: all 0.3s;
    }
    #sidebar.active {
        margin-left: -300px;
    }
    .footer {
        position: absolute;
        bottom: 0;
        width: 90%;
    }
</style>
