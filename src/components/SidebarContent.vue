<template>
  <q-list>
    <q-item>
      <sidebar-project-select :project-list="projectList" />
    </q-item>

    <q-item class="q-mt-xs">
      <sidebar-drop-select :policy-list="policyList" />
    </q-item>

    <q-item class="q-mt-xs">
      <sidebar-serial-select v-if="distribution" />
    </q-item>

    <q-item class="q-mt-xs">
      <sidebar-rank-filter v-if="distribution" />
    </q-item>

    <q-item class="dist-wrapper q-mt-xs">
      <distribution
        v-if="distribution"
        :distribution="distribution"
      />
    </q-item>

    <q-item class="fixed-bottom">
      <donate-modal />
    </q-item>
  </q-list>
</template>

<script>
import Distribution from "./Distribution.vue";
import DonateModal from "./DonateModal.vue";
import SidebarProjectSelect from "./SidebarProjectSelect.vue";
import SidebarDropSelect from "./SidebarDropSelect.vue";
import SidebarSerialSelect from "./SidebarSerialSelect.vue";
import SidebarRankFilter from "./SidebarRankFilter.vue"
import { mapState } from "vuex";

export default {
  name: "SidebarContent",

  components: {
    SidebarRankFilter,
    SidebarSerialSelect,
    SidebarProjectSelect,
    SidebarDropSelect,
    Distribution,
    DonateModal,
  },

  computed: {
    ...mapState(["projectList", "policyList", "distribution"]),
  },

};
</script>


<style lang="scss" scoped>
</style>
