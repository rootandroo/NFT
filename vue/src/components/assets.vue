<template>
    <b-card-group 
     :next="next"
     @scroll.passive="fetchNextPage(next)"
     class="pl-4 pb-4">
        <b-card 
         v-for="asset in assets" 
         :key="asset.name"
         :img-src="fetchImagePath(asset.onchain_metadata.image)"
         class="mr-4 mt-4 p-2 bg-light rounded text-dark-accent">
            {{ asset.onchain_metadata.name }} 
        </b-card>
    </b-card-group>    
</template>

<script>
import axios from 'axios'
const URLS = JSON.parse(document.getElementById('json_data').textContent).urls
const headers = {'Authorization':'Token'.concat(' ', process.env.VUE_APP_TOKEN)}

export default {
    name: 'assets',
    methods: {
        fetchAssets: function(event) {
            axios
                .get(URLS.list_asset, { params: { policy_id: event} }, { headers:headers })
                .then(response => {
                    this.assets = response.data.results
                    this.next = response.data.next
                    this.fetchDistribution(event)
                })
        },
        fetchNextPage: function(url) {
            var elm = document.querySelector('.card-group')
            var distance = elm.scrollTop
            var offset = elm.offsetHeight
            var height = elm.scrollHeight
            if (distance + offset >= height - 1) {
                axios
                    .get(url, {headers:headers})
                    .then(response => {
                        this.assets.push(...response.data.results)
                        this.next = response.data.next
                    })
            }
        },
        fetchImagePath: ipfs => {
            if (ipfs.includes("/")) {
                var index = ipfs.lastIndexOf("/")
                ipfs = ipfs.substr(index + 1)
            }
            var url = 'https://ipfs.blockfrost.dev/ipfs/' + ipfs
            return url
        },
        fetchDistribution: function(policy_id) {
            axios
                .get(URLS.list_collection + policy_id, {headers:headers})
                .then(response => {
                    this.distribution =  response.data.distribution
                })
        } 
    },
    data () {
        return {
            assets: null,
            next: null,   
            distribution: null,
        }
    },
    created () {
        this.$root.$on('fetch-assets', (event) => {
            this.assets = null
            this.next = null
            this.fetchAssets(event)
        })
    }
}
</script>

<style scoped>
    .card-group {
        display: grid;
        overflow-y: auto;
        height: calc(100% - 68px - 10px);
        grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
    }

    .card-group::-webkit-scrollbar {
        width: 20px;
    }
    .card-group::-webkit-scrollbar-thumb {
        background-color: #74eda5;
        border-radius: 20px;
        border: 6px solid transparent;
        background-clip: content-box;
    }
    .card, img {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        text-align: center;
    }
</style>