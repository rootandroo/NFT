<template>
    <transition name="asset-list">
        <div id="asset-wrapper" v-if="assets">
            <transition-group 
            v-if="assets"
            :next="next" 
            tag="div"
            name="list-append"
            class="pl-4 pb-4 card-group">
                <b-card
                v-for="asset in assets" 
                :key="asset.name"
                :img-src="fetchImagePath(asset.onchain_metadata.image)"
                class="mr-4 mt-4 p-2 bg-light rounded text-dark-accent">
                    {{ asset.onchain_metadata.name }} 
                </b-card>
            </transition-group>
            <div id="observe" v-if="assets" :key="next" v-observe-visibility="handleScroll"></div>
        </div>
    </transition>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
const URLS = JSON.parse(document.getElementById('json_data').textContent).urls
const headers = {'Authorization':'Token'.concat(' ', process.env.VUE_APP_TOKEN)}

export default {
    name: 'TheAssetList',
    data: function () {
        return {
            assets: null,
            next: null,   
        }
    },


    created: function () {
        this.$root.$on('fetch-assets', (policy_id, queryList=null) => {
            this.assets = null
            setTimeout(function () {
                 this.fetchAssets(policy_id, queryList) }.bind(this), 500)
        })
    },


    beforeDestroy: function () {
        this.$$root.$off('fetch-assets', (policy_id, queryList=null) => {
            this.assets = null
            setTimeout(function () {
                 this.fetchAssets(policy_id, queryList) }.bind(this), 500)
        })
    },


    methods: {
        fetchAssets: function(policy_id, queryList=null) {
            axios
                .get(URLS.list_asset, { params: {
                     policy_id: policy_id,
                     query_list: queryList }}, { headers:headers })
                .then(response => {
                    this.next = response.data.next
                    this.assets = response.data.results
                })
        },

        fetchNextPage: _.throttle(function() {
            var url = this.next
            axios
                .get(url, {headers:headers})
                .then(response => {
                    this.assets.push(...response.data.results)
                    this.next = response.data.next
                })
        }, 1500),

        fetchImagePath: ipfs => {
            if (ipfs.includes("/")) {
                var index = ipfs.lastIndexOf("/")
                ipfs = ipfs.substr(index + 1)
            }
            var url = 'https://ipfs.blockfrost.dev/ipfs/' + ipfs
            return url
        },

        handleScroll: function (isVisible) {
            if (!isVisible) { return }
            this.fetchNextPage()
        }
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