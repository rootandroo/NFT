<template>
  <q-page v-if="collection">
    <q-infinite-scroll
      :offset="250"
      :debounce="700"
      @load="onLoad"
    >
      <div
        class="card-group q-pa-lg q-gutter-md"
        :v-if="assetList"
      >
        <q-intersection
          v-for="asset in assetList"
          :key="asset.name"
          transition="fade"
        >
          <asset-card :asset="asset" />
        </q-intersection>
      </div>
    </q-infinite-scroll>
  </q-page>
</template>

<script>
import AssetCard from "../components/AssetCard.vue";
import { mapActions, mapState, mapMutations, mapGetters } from "vuex";

export default {
  components: {
    AssetCard,
  },

  data() {
    return {
      nextPage: null,
    };
  },

  computed: {
    ...mapState("api", [
      "nextURL",
      "collection"
    ]),

    ...mapState(["assetList"]),

    ...mapGetters('api', ["createValues"])
  },

  watch: {
    "$route.params.project"(project) {
      this.collectionRouteMatch(project, this.$route.params.drop)
    },
    collection(newCol, oldCol) {
      console.log(`Updating from ${oldCol?.policy_id} to ${newCol.policy_id}`);
      this.$router.push({ path: `/${this.$route.params.project}/${newCol.name.replace(/ /g,'_')}`})

      //  Reset Filters
      this.updateTags([]);
      this.updatePriceFilter({ min: null, max: null });
      this.updateRankFilter({ min: null, max: null });

      this.fetchAssets().then((resp) => {
        this.updateCirculation(resp.found);
      });
      var distribution = this.collection?.distribution
      if (distribution) { this.updateValues(this.createValues(distribution)) }
    },
  },

  created() {
    this.collectionRouteMatch(this.$route.params.project, this.$route.params.drop)
  },

  methods: {
    ...mapActions("api", [
      "fetchCollections",
      "fetchAssets",
      "fetchDistribution",
    ]),

    ...mapMutations("api", [
      "updateValues",
      "updateCollection",
      "updateTags",
      "updateCirculation",
      "updatePriceFilter",
      "updateRankFilter",
    ]),

    // Match route params to collection
    collectionRouteMatch (project, drop) {
      var drop = drop.replace(/_/g, " ");
      this.fetchCollections(project).then(collections => {
        var collection = collections.filter(col => { return col.name == drop })
        if (collection.length) {
          this.updateCollection(collection[0])
        } else {
          this.updateCollection(collections[0])
        }
      })
    },

    onLoad (index, done) {
      if (this.nextURL) {
        this.fetchAssets({ append: true });
      }
      done();
    },
  },
};
</script>

<style>
.card-group {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
}

.q-intersection {
  min-height: 285px;
}
</style>

