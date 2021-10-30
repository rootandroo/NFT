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
      <q-item-section v-if="distribution">
        <q-item-label class="text-white text-body1">
          Filters
        </q-item-label>
        <sidebar-rank-filter />
        <sidebar-price-filter />
      </q-item-section>
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
import SidebarPriceFilter from "./SidebarPriceFilter.vue"

import { mapState } from "vuex";

export default {
  name: "SidebarContent",

  components: {
    SidebarPriceFilter,
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
