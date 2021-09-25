<template>
    <div id='sidebar' :class="['bg-secondary', 'sticky-top', {'active':is_active}]">
        <b-form-group class="w-100 px-3 mt-3" inline>
            <h3 class="text-dark">Select Project</h3>
            <b-form-select 
                class="mb-5" 
                :options="projects"
                @change="fetchPolicies">
                </b-form-select>
            <h3 class="text-dark">Select Policy</h3>
            <b-form-select
                :options="policies"
                @change="emitAssets"></b-form-select>
        </b-form-group>
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
                console.log(response.data.results)
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
          is_active: true,
      }
  },
  created () {
      this.$root.$on('toggle-sidebar', () => {
          this.is_active = !this.is_active
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
        transition: all 0.5s;
    }
    #sidebar.active {
        margin-left: -300px;
    }
</style>
