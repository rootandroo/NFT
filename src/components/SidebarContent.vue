<template>
  <q-scroll-area class="fit">
    <q-list>
      <q-item>
        <q-item-section>
          <h6 class="title">
            Select Project
          </h6>
          <q-select
            v-model="project"
            color="white"
            dense
            options-dense
            dark
            use-input
            fill-input
            hide-selected
            :options="projects"
            @update:model-value="val => { handleProjectSelect(val) }" 
            @filter="filterFn"
          />
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section>
          <h6 class="title">
            Select Policy
          </h6>
          <div style="max-width: 268px">
            <q-select
              v-model="policyID"
              color="white"
              dense
              options-dense
              dark
              :options="policyList"
              @update:model-val="updatePolicyID(policyID)"
            >
              <template #selected-item="scope">
                <div class="ellipsis">
                  {{ scope.opt }}
                </div>
              </template>
            </q-select>
          </div>
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section>
          <q-input
            v-model="serialInput"
            color="white"
            label="Search By Serial"
            label-color="white"
            dense
            type="number"
            dark
          />
        </q-item-section>
      </q-item>

      <q-item>
        <distribution />
      </q-item>

      <q-item class="fixed-bottom">
        <donate-modal />     
      </q-item>
    </q-list>
  </q-scroll-area>
</template>

<script>
import Distribution from './Distribution.vue'
import DonateModal from './DonateModal.vue'
import { mapState, mapMutations } from 'vuex'

export default {
    name: 'SidebarContent',

    components: {
        Distribution,
        DonateModal
    },

    data () {
        return {
            project: null,
            projects: []
        }
    },

    computed: {
      ...mapState([
          'projectList',
          'policyList',
      ]),

      ...mapState('api', [
        'policyID',
        'serial'
      ]),

      serialInput: {
        get () {
          return this.serial
        },
        set (val) {
          this.updateSerial(val)
        }
      }
    },

    methods: {
        handleProjectSelect (project) {
            this.$router.push({ path: `/${project.replace(/ /g,'')}`})
        },

        ...mapMutations('api', [
            'updatePolicyID',
            'updateSerial'
        ]),

        filterFn (val, update) {
            if (val === '') {
                update(() => {
                    this.projects = this.projectList
                })
                return
            }

            update(() => {
                const needle = val.toLowerCase()
                this.projects = this.projectList.filter(v => v.toLowerCase().indexOf(needle) > -1)
            })
        },
    }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
    .title {
        color: white;
        margin-top: 5px;
        margin-bottom: 0px;
    }
</style>
