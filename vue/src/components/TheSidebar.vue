<template>
    <div id='sidebar' :class="['d-flex', 'flex-column', 'bg-dark', 'sticky-top', 'px-3', {'active':sidebar}]">
        <b-row>
            <b-form-group class="w-100 p-3 mb-2" inline>
                <h5 class="text-light">Select Project</h5>
                <b-form-select class="mb-3 bg-light"
                    size="sm"
                    v-model="project" 
                    :options="projects"
                    @change="fetchPolicies">
                    </b-form-select>
                <transition name="item" appear>
                    <div class="policy-wrapper" v-if="project">
                        <h5 class="text-light">Select Policy</h5>
                        <b-form-select class="bg-light"
                            size="sm"
                            v-model="policyID"
                            :options="policies"
                            @change="handlePolicyChange">
                        </b-form-select>
                    </div>
                </transition>
            </b-form-group>
        </b-row>
        <b-row>
            <the-distribution 
             :policyID="policyID"/>
        </b-row>
        <b-row class="mt-auto mb-3"> 
            <b-col>
                <b-button class="mt-2 text-dark" block>Donate</b-button>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import axios from 'axios'
import TheDistribution from './TheDistribution.vue'
const URLS = JSON.parse(document.getElementById('json_data').textContent).urls
const headers = {'Authorization':'Token'.concat(' ', process.env.VUE_APP_TOKEN)}

export default {
  name: 'TheSidebar',
  components: {
      TheDistribution
  },
  data: function () {
      return {
          sidebar: true,
          projects: null,
          project: '',
          policies: null,
          policyID: '',
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
  },

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
      handlePolicyChange: function () {
          this.$root.$emit('policyIDUpdate', this.policyID)
      },
  },
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
    #sidebar {
        min-width: 300px;
        max-width: 300px;
        height: 100%;
        transition: all 0.3s;
        overflow-y: auto;
    }
    #sidebar::-webkit-scrollbar {
        width: 20px;
    }

    #sidebar::-webkit-scrollbar-thumb {
        background-color: white;
        border-radius: 20px;
        border: 6px solid transparent;
        background-clip: content-box;
    }

    #sidebar.active {
        margin-left: -300px;
    }
    
    .item-enter-active, .item-leave-active {
        transition: opacity 1s ease-in-out;
    }
    
    .item-enter, .item-leave-to {
        opacity: 0;
    }
</style>
