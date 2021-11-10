<template>
  <q-item-section>
    <q-select
      v-model="project"
      label="Select Project"
      options-dense
      dark
      label-color="white"
      use-input
      fill-input
      hide-selected
      options-selected-class="text-positive"
      popup-content-class="options"
      :options="projects"
      @update:model-value="val => { handleProjectSelect(val) }" 
      @filter="filterFn"
    />
  </q-item-section>
</template>

<script>
export default {

    props: {
        projectList: {
            type: Array,
            required: true
        }
    },

    data () {
        return {
            project: null,
            projects: []
        }
    },

    methods: {
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
    }


}
</script>

<style>
.options {
  -ms-overflow-style: none;
  scrollbar-width: none; 
  overflow-y: scroll; 
}

.options::-webkit-scrollbar {
  display: none;
}
</style>