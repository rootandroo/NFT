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
             :urls="urls"
             :policyID="policyID"
             :headers="headers"/>
        </b-row>
        <b-row class="mt-auto mb-3"> 
            <b-col>
                <b-button v-b-modal.donate class="mt-2 text-dark" block>Donate</b-button>
            </b-col>
            <b-modal id="donate" body-bg-variant="dark" size="lg" centered hide-header hide-footer>
                <h5 class="text-light mr-0 text-center">ADA Donations Support Further Development</h5>
                <b-card bg-variant="dark-accent">
                    <b-row no-gutters>
                        <b-col md="4">
                            <b-img thumbnail fluid :src="donate" alt="QRCode"></b-img>
                        </b-col>
                        <b-col md="8">
                            <b-card-body class="text-dark" title="Donations Are Appreciated">
                            <b-card-text>
                                Please do not send ADA from an exchange. Only send ADA from a supported wallet i.e. Daedalus, Yoroi, or Adalite.
                            </b-card-text>
                                <span class="mt-2"> 
                                    {{ this.address }}
                                </span>
                            </b-card-body>
                        </b-col>
                    </b-row>
                </b-card>
            </b-modal>
        </b-row>
    </div>
</template>

<script>
import QRCode from 'qrcode'
import axios from 'axios'
import TheDistribution from './TheDistribution.vue'

export default {
  name: 'TheSidebar',
  
  components: {
      TheDistribution
  },

  props: {
      headers: Object,
      urls: Object
  },

  data: function () {
      return {
          sidebar: false,
          projects: null,
          project: '',
          policies: null,
          policyID: '',
          address: 'addr1qxufz8nu0s6my5rvqns3xjsupfcua4uw4l5p0jc69hlp8de92xc8xqrc9xlv798vg95y47p2w243e3lwj8vnd8f2rlrsy8fs04',
          donate: ''
      }
  },


  created () {
      this.fetchProjects()
      this.$root.$on('toggle-sidebar', () => {
          this.sidebar = !this.sidebar
      });
      this.fetchAdaUrl()
  },


  beforeDestroy() {
    // removing $root listener
    this.$root.$off('toggle')
  },

  methods: {
      fetchProjects: function() { 
        axios
            .get(this.urls.list_project, { headers: this.headers })
            .then(response => {
                this.projects = response.data.results.map(
                    project => project.name)
            })
      },

      fetchPolicies: function() {
          var params = { project: this.project}
          axios
            .get(this.urls.list_collection, { params:params }, { headers:this.headers })
            .then(response => {
                this.policies = response.data.results.map(
                    collection => collection.policy_id) 
            })
      },

      handlePolicyChange: function () {
          this.$root.$emit('policyIDFromSidebar', this.policyID)
      },

      fetchAdaUrl: function () {
          QRCode.toDataURL(this.address)
          .then(url => {
              this.donate = url
          })
      }
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
