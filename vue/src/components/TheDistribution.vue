<template>
    <transition v-if="distribution" name="dist" mode="out-in" appear>
                <div class="attribute-list-wrapper w-100">
                    <h5 class="w-100 px-3 text-light">Distribution</h5>
                    <b-form-checkbox-group
                     id="checkbox-wrapper"
                     v-model="queryArray"
                     @change="handleQueryUpdate"
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
                                v-b-toggle="removeSpaces(trait)"
                                size="sm">{{ getLabel(trait) }}
                            </b-button>
                            <b-collapse 
                             :id="removeSpaces(trait)" 
                             class="pr-4">
                                <b-row class="pl-4"
                                v-for="[option, count] in Object.entries(obj)"
                                :key="option">

                                    <b-form-checkbox class="checkbox border-0 mb-1"
                                    :value="{[trait]:option}"
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
    policyID: String
  },
  data: function () {
      return {
          distribution: null,
          queryArray: []
      }
  },
  computed: {
      getLabel: function () {
          return trait => {
              var re = /[^_]*$/
              return re.exec(trait)[0]
          }
      },
      removeSpaces: function () {
          return string => {
              return string.replace(/\s+/g, '')
          }
      }
  },
  watch: {
    policyID: function (val) {
        this.distribution = null
        this.queryArray = []
        this.setDistribution(val)
    },
  },
  methods: {      
      setDistribution: function (policyID) {
          axios
            .get(URLS.list_collection + policyID, {headers:headers})
            .then(response => {
                this.distribution = response.data.distribution
            })
      },
      handleQueryUpdate: function () {
        this.$root.$emit('queryArrayUpdate', this.queryArray)
      },
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

    .dist-enter-active, .dist-leave-active {
        transition: opacity .5s ease-in-out;
    }
    
    .dist-enter, .dist-leave-to {
        opacity: 0;
    }
</style>
