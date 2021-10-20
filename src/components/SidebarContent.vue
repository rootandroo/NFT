<template>
  <q-list>
    <q-item>
      <q-item-section>
        <q-item-label class="text-white text-h6">
          Select Project
        </q-item-label>
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
        <q-item-label class="text-white text-h6">
          Select Policy
        </q-item-label>
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
          debounce="500"
          @update:model-value="handleSerialUpdate"
        />
      </q-item-section>
    </q-item>

    <q-item class="dist-wrapper"> 
      <q-scroll-area class="fit">
        <distribution v-if="distribution" />
      </q-scroll-area>
    </q-item>

    <q-item class="fixed-bottom">
      <donate-modal />     
    </q-item>
  </q-list>
</template>

<script>
import Distribution from './Distribution.vue'
import DonateModal from './DonateModal.vue'
import { mapState, mapMutations, mapActions } from 'vuex'

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
          'distribution'
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
        ...mapMutations('api', [
          'updatePolicyID',
          'updateSerial'
        ]),

        ...mapActions('api', [
          'fetchAssets'
        ]),

        handleProjectSelect (project) {
            this.$router.push({ path: `/${project.replace(/ /g,'')}`})
        },

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

        handleSerialUpdate (serial) {
          this.fetchAssets({policyID:this.policyID, serial:this.serial})
        }
    }
}
</script>


<style lang="scss" scoped>
.dist-wrapper {
    height: calc(100vh - 275px);
}
</style>
