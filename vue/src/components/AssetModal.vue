<template>
    <b-modal :id="asset.name" size="lg" class="border-0" body-bg-variant="dark" hide-header hide-footer centered>
        <b-container>
            <b-row>
                <b-col class="mb-3" md="7">
                    <b-card
                        class="px-2 pt-2 text-dark"
                        :img-src="src">
                        {{ name }}
                    </b-card>
                </b-col>

                <b-col v-if="keys" md="5">
                    <b-container>
                        <div class="rarity p-2 mb-3 text-center">
                            <h5 class="text-dark text-center">Rarity Score</h5>
                            <b-badge class="score w-100 text-secondary">
                                <h6 class="mb-0">
                                    {{ asset.score }}
                                </h6>
                            </b-badge>
                        </div>

                        <b-row class="mb-2"
                            v-for="key in Object.keys(keys)"
                            :key="key"> 
                            <span>
                                <!-- Trait Label -->
                                <b-button class="mb-1 text-dark mr-2"
                                    variant="light"
                                    size="sm">{{ getLabel(key) }}
                                </b-button>
                                <b-button class="mb-1 text-dark mr-2"
                                    v-if="!Array.isArray(getValues(key))"
                                    variant="light"
                                    size="sm">
                                    {{ getValues(key) }}
                                    <b-badge class="bg-secondary">
                                        {{ getCount(key, getValues(key)) }}
                                    </b-badge>
                                </b-button>
                                <!-- Trait Values -->
                                <b-button class="mb-1 text-dark mr-2"
                                    v-else 
                                    v-for="value in getValues(key)"
                                    :key="value"
                                    variant="light"
                                    size="sm">
                                    {{ value }}
                                    <b-badge class="bg-secondary">
                                        {{ getCount(key, value) }}
                                    </b-badge>
                                </b-button>
                            </span>
                        </b-row>
        
                    </b-container>
                </b-col>

            </b-row>
        </b-container>
    </b-modal>   
</template>

<script>
export default {
    name: 'AssetModal',
    props: {
        asset: {
            type: Object
        },
        keys: {
            type: Object
        },
        distribution: {
            type: Object
        },
        name: {
            type: String
        },
        src: {
            type: String
        },
    },
    computed: {
        // gets the label of the trait where key = '..._label'
        getLabel: function () {
            return key => {
                var re = /[^_]*$/
                return re.exec(key)[0]
            }
        },
    },

    methods: {
        // Returns value for a given trait, returns 'None' if the trait is 
        // not in the assets metadata
        getValues: function (key) {
            return (key in this.asset.onchain_metadata) ? this.asset.onchain_metadata[key]
            : 'None'
        },

        // Returns frequency of a given trait:value
        getCount: function (key, value) {
            value = Object.is(value, 'None') ? null : value
            return (this.distribution[key][value])
        },
    },
}
</script>

<style lang="scss" scoped>
    .card {
	box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
	text-align: center;
        .card-body {
            padding: 10px;
        }
    }
    .card-img {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        text-align: center;
    }

    .rarity {
        background-color: #74eda5;
        border-radius: 0.25rem;
        .score {
            background-color: #F5F4F4;
        }
    }
</style>