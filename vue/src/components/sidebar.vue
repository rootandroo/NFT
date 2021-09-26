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
                  v-model="selected"
                  class="bg-light"
                  :options="policies"
                  @change="emitAssets">
                </b-form-select>
                <div v-if="selected" class="mt-5 text-center">
                    <b-button variant="light">View Rarity</b-button>
                </div>
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
      emitAssets: function(event) {
          this.$root.$emit('fetch-assets', event)
      },
  },
  data () {
      return {
          projects: null,
          policies: null,
          sidebar: true,
          selected: ''
      }
  },
  created () {
      this.$root.$on('toggle-sidebar', () => {
          this.sidebar = !this.sidebar
      });

      // fetch project names 
      axios
        .get(URLS.list_project, { headers: headers })
        .then(response => {
            this.projects = response.data.results.map(
                project => project.name)
        })
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
