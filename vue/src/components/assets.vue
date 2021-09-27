<template>
    <transition name="list" v-on:enter="addScrollListener">
    <transition-group 
     mode="out-in"
     v-if="assets"
     name="list" 
     class="pl-4 pb-4 card-group" 
     tag="div"
     :next="next">
        <b-card
         v-for="asset in assets" 
         :key="asset.name"
         :img-src="fetchImagePath(asset.onchain_metadata.image)"
         class="list-item mr-4 mt-4 p-2 bg-light rounded text-dark-accent">
            {{ asset.onchain_metadata.name }} 
        </b-card>
    </transition-group>
    </transition>
</template>

<script>
import _ from 'lodash'
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
                    this.next = response.data.next
                    this.assets = response.data.results
                })
        },
        fetchNextPage: _.throttle(function() {
            var url = this.next
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
        }, 1500),
        fetchImagePath: ipfs => {
            if (ipfs.includes("/")) {
                var index = ipfs.lastIndexOf("/")
                ipfs = ipfs.substr(index + 1)
            }
            var url = 'https://ipfs.blockfrost.dev/ipfs/' + ipfs
            return url
        },
        addScrollListener: function () {
            document.querySelector('.card-group').addEventListener('scroll', () => this.fetchNextPage())
        }
    },
    data () {
        return {
            assets: null,
            next: null,   
        }
    },
    created () {
        this.$root.$on('fetch-assets', (event) => {
            this.assets = null
            setTimeout(function () { this.fetchAssets(event) }.bind(this), 1000)
        })
    },
    destroyed () {
        document.querySelector('.card-group').removeEventListener('scroll', () => this.fetchNextPage())
        this.$$root.$off('fetch-assets', (event) => {
            this.fetchAssets(event)
        })
    }
}
</script>

<style lang="scss" scoped>
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
        background-color: white;
        border-radius: 20px;
        border: 6px solid transparent;
        background-clip: content-box;
    }
    .card, img {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        text-align: center;
    }

    .list-item {
        display: inline-block;
        margin-right: 10px;
    }
    
    .list-enter-active, .list-leave-active {
        transition: opacity 1s;
    }
    
    .list-enter, .list-leave-to {
        opacity: 0;
    }
</style>