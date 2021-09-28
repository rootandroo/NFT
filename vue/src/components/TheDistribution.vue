<template>
    <transition v-if="distribution" name="item" mode="out-in" appear>
                <div class="attribute-list-wrapper w-100">
                    <h5 class="w-100 px-3 text-light">Distribution</h5>
                    <b-form-checkbox-group
                     id="checkbox-wrapper"
                     v-model="queryList"
                     size="sm"
                     buttons
                     stacked
                     button-variant="light">
                        <div class="mb-1 px-3"
                        v-for="[trait, obj] of Object.entries(distribution)"
                        :key="trait">
                        
                            <!-- Trait List Button -->
                            <b-button class="mb-1 text-dark"
                                variant="light"
                                v-b-toggle="trait"
                                size="sm">{{trait}}
                            </b-button>
                            <b-collapse :id="trait">
                                <b-row class="pl-4"
                                v-for="[option, count] in Object.entries(obj)"
                                :key="option">

                                    <b-form-checkbox class="checkbox border-0 mb-1"
                                    :value="createQuery(trait, option)" 
                                    hidden>
                                        <span class="text-dark">
                                            {{option}}
                                            <b-badge class="bg-secondary">
                                                {{count}}
                                            </b-badge>
                                        </span>
                                    </b-form-checkbox>

                                </b-row>
                            </b-collapse>

                        </div>
                    </b-form-checkbox-group>
                </div>
    </transition>
</template>

<script>
import axios from 'axios'
const URLS = JSON.parse(document.getElementById('json_data').textContent).urls
const headers = {'Authorization':'Token'.concat(' ', process.env.VUE_APP_TOKEN)}

export default {
  name: 'TheDistribution',
  props: {
    policy_id: String
  },
  data: function () {
      return {
          distribution: null,
          queryList: []
      }
  },
  watch: {
    policy_id: function (val) {
        this.distribution = null
        setTimeout(function () {
            this.setDistribution(val)}.bind(this), 50)
    },
    queryList: function(val) {
        this.$emit('queryListFromDist', val)
    }
  },
  methods: {      
      setDistribution: function (policy_id) {
          axios
            .get(URLS.list_collection + policy_id, {headers:headers})
            .then(response => {
                this.distribution = response.data.distribution
            })
      },
      createQuery: function (trait, option) {
          let query = {}
          query[trait] = option
          return query
      }
  },
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
    .checkbox.active  {
        background-color: #74eda5 !important;
        span {
            color: #F5F4F4 !important;
            .badge {
                color: #8D4D72 !important;
                background-color: #F5F4F4 !important;
            }
        }
    }
</style>
