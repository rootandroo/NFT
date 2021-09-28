<template>
    <div id="asset-wrapper">
    <transition v-if="assets" name="list">
    <transition-group 
     v-if="assets"
     :next="next" 
     tag="div"
     name="list"
     class="pl-4 pb-4 card-group">
        <b-card
         v-for="asset in assets" 
         :key="asset.name"
         :img-src="fetchImagePath(asset.onchain_metadata.image)"
         class="mr-4 mt-4 p-2 bg-light rounded text-dark-accent">
            {{ asset.onchain_metadata.name }} 
        </b-card>
    </transition-group>
    </transition>
    <div id="observe" v-if="assets" :key="next" v-observe-visibility="handleScroll"></div>
    </div>
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
            console.log(queryList)
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
    #asset-wrapper {
        overflow-y: auto;
        height: calc(100% - 68px - 10px);
    }
    #asset-wrapper::-webkit-scrollbar {
        width: 20px;
    }

    #asset-wrapper::-webkit-scrollbar-thumb {
        background-color: white;
        border-radius: 20px;
        border: 6px solid transparent;
        background-clip: content-box;
    }
    .card-group {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
    }

    .card, img {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        text-align: center;
    }
    
    .list-enter-active, .list-leave-active {
        transition: opacity .5s ease-in-out;
    }
    
    .list-enter, .list-leave-to {
        opacity: 0;
    }
</style>