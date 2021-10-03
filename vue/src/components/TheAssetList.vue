<template>
    <transition mode="out-in" name="asset-list" appear>
        <div id="asset-wrapper" v-if="assets">
            <transition-group 
             :next="next" 
             tag="div"
             name="list-append"
             v-if="assets"
             class="pl-4 pb-4 card-group">
                <b-card
                 v-for="asset in assets" 
                 :key="asset.name"
                 :img-src="fetchImagePath(asset.onchain_metadata.image)"
                 class="mr-4 mt-4 px-2 pt-2 bg-light rounded text-dark-accent">
                    {{ getAssetName(asset) }}
                    <a v-b-modal="asset.name" class="stretched-link"></a>
                    <asset-modal
                     :keys="keys"
                     :asset="asset"
                     :name="getAssetName(asset)"
                     :src="fetchImagePath(asset.onchain_metadata.image)"
                     :distribution="distribution"/>
                </b-card>
            </transition-group>
            <div id="observe" v-if="assets" :key="next" v-observe-visibility="handleScroll"></div>
        </div>
    </transition>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import AssetModal from './AssetModal.vue'

export default {
  components: { AssetModal },
    name: 'TheAssetList',
    props: {
        headers: Object,
        urls: Object
    },
    data: function () {
        return {
            assets: null,
            next: false,   
            queryObj: null,
            policyID: null,
            keys: null,
            distribution: null,
        }
    },

    
    computed: {
        getAssetName ()  {
            return asset => asset.onchain_metadata.title ?? asset.onchain_metadata.name
        }
    },


    created: function () {
        this.$root.$on('queryObjFromDist', (query) => {
            this.handleQueryUpdate(query)
        })


        this.$root.$on('policyIDFromSidebar', (policyID) => {
            this.handlePolicyUpdate(policyID)
        })

        this.$root.$on('distObjFromDist', (distObj) => {
            this.distribution = distObj
        })
    },


    beforeDestroy: function () {
        this.$root.$off('queryObjFromDist', (query) => {
            this.handleQueryUpdate(query)
        })


        this.$root.$off('policyIDFromSidebar', (policyID) => {
            this.policyID = policyID
            this.handlePolicyUpdate(policyID)
        })
    },


    methods: {
        fetchAssets: function () {
            var config = { 
                headers: this.headers,
                params: {
                    policy_id: this.policyID, 
                    query_obj: this.queryObj
                }
            }
            
            axios
                .get(this.urls.list_asset, config)
                .then(response => {
                    this.next = response.data.next
                    this.assets = response.data.results
                })
        },

        fetchNextPage: _.throttle(function() {
            if (!this.next) { return } // no policyID selected
            const params = { queryObj: this.queryObj }
            axios
                .get(this.next, { params: params }, {headers:this.headers})
                .then(response => {
                    this.assets.push(...response.data.results)
                    this.next = response.data.next
                })
        }, 1500),

        handleQueryUpdate: function (query) {
            const objArray = JSON.parse(JSON.stringify(query))
            const queryObj = objArray.reduce(this.merge, {})
            this.queryObj = queryObj
            setTimeout(function () {
                 this.fetchAssets() }.bind(this), 500)
        },

        handlePolicyUpdate: function (policyID) {
            this.assets = null
            this.queryObj = null
            this.keys = null
            this.policyID = policyID
            this.setKeys()
            setTimeout(function () {
                 this.fetchAssets() }.bind(this), 500)
        },

        setKeys: function () {
            axios.get(this.urls.list_collection + this.policyID, {headers:this.headers})
            .then(response => {
                this.keys = response.data.included_keys
            })
        },

        fetchImagePath: function (ipfs) {
            var ipfs_id = /[^/]*$/.exec(ipfs)[0];
            return 'https://ipfs.blockfrost.dev/ipfs/' + ipfs_id
        },


        handleScroll: function (isVisible) {
            if (isVisible) {
                this.fetchNextPage()
            }
        },

        merge: function (a,b) {
            for (const key in b) {
                if (key in a) {
                    if (Array.isArray(a[key])) {
                        a[key].push(b[key])
                    } else {
                        a[key] = new Array(a[key], b[key])
                    }
                } else {
                    if (this.keys[key]) {
                        a[key] = new Array(b[key])
                    } else {
                        a[key] = b[key]
                    }
                }
            }
            return a
        },
    },
}
</script>

<style lang="scss" scoped>
.card-group {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
}
.card {
	box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
	text-align: center;
    .card-body {
        padding: 10px;
    }
}
img {
	box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
	text-align: center;
}

.asset-list-enter-active {
	transition: opacity .5s ease-in-out;
}
.asset-list-leave-active {
	transition: opacity .5s ease-in-out;
}
.asset-list-enter {
	opacity: 0;
}
.asset-list-leave-to {
	opacity: 0;
}


.list-append-enter-active {
	transition: opacity 1.5s ease-in-out;
}
.list-append-leave-active {
	transition: opacity 1.5s ease-in-out;
}
.list-append-enter {
	opacity: 0;
}
.list-append-leave-to {
	opacity: 0;
}
#asset-wrapper {
	overflow-y: auto;
	height: calc(100% - 68px - 10px);
	&::-webkit-scrollbar {
		width: 20px;
	}
	&::-webkit-scrollbar-thumb {
		background-color: white;
		border-radius: 20px;
		border: 6px solid transparent;
		background-clip: content-box;
	}
}
</style>