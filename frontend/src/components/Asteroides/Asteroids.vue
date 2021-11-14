<template>
    <b-row>
        <b-col>
            <b-table striped :items="asteroids" :fields="fields">
                <template v-slot:cell(body)="data">
                    <div class="asteroid" v-html="matrix(data.item.body)"></div>
                </template>
            </b-table>

        </b-col>
    </b-row>
</template>

<script>
import messagesService from '@/services/messagesService'

export default {
    name: 'Asteroids',
    data () {
        return {
            fields: [
                {
                    key: 'id',
                    label: 'Id'
                },
                {
                    key: 'body',
                    label: 'Body',
                    formatter: 'matrix'
                },
                {
                    key: 'sighting',
                    label: 'Sightings count',
                    formatter: 'count_sighting'
                }
            ],
            asteroids: []
        }
    },
    created () {
        this.update()
    },
    methods: {
        update () {
            messagesService.fetchAsteroids().then((data) => {
                this.asteroids = data
            })
        },
        count_sighting (value, key, item) {
            if (typeof value === 'undefined') return ''
            return value.length
        },
        matrix (value, key, item) {
            if (typeof value === 'undefined') return ''
            return JSON.stringify(value, undefined, '\t').replace(/]|[[]/g, '').replace(/,\n/g, '').replace(/\n\n/g, '\n').replace(/1/g, '<div class="square bg-dark"></div>').replace(/0/g, '<div class="square bg-lesslight"></div>').trim().replace(/\n/g, '</br>').replace(/^\t\t/gm, '')
        }
    }
}
</script>

<style scoped>

</style>
