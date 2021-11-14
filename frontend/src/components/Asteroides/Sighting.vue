<template>
    <b-row>
        <b-col>
            <b-table striped :items="sightings" :fields="fields">
                <template v-slot:cell(asteroid.body)="data">
                    <div class="asteroid" v-html="matrix(data.item.asteroid.body)"></div>
                </template>
            </b-table>

        </b-col>
    </b-row>
</template>

<script>
import messagesService from '@/services/messagesService'

export default {
    name: 'Sighting',
    data () {
        return {
            fields: [
                {
                    key: 'id',
                    label: 'Id',
                    sortable: true
                },
                {
                    key: 'asteroid.body',
                    label: 'Asteroid',
                    formatter: 'matrix'
                },
                {
                    key: 'observatory.id',
                    label: 'Observatory'
                },
                {
                    key: 'device.id',
                    label: 'Device'
                },
                {
                    key: 'device.device_resolution',
                    label: 'Device'
                },
                {
                    key: 'device.observatory',
                    label: 'Device'
                },
                {
                    key: 'date',
                    label: 'Date',
                    sortable: true
                },
                {
                    key: 'time',
                    label: 'Time',
                    sortable: true
                },
                {
                    key: 'matrix',
                    label: 'Matrix'
                }
            ],
            sightings: []
        }
    },
    created () {
        this.update()
    },
    methods: {
        update () {
            messagesService.fetchSighting().then((data) => {
                this.sightings = data
            })
        },

        matrix (value, key, item) {
            return (typeof value === 'undefined') ? '' : JSON.stringify(value, undefined, '\t').replace(/]|[[]/g, '').replace(/,\n/g, '').replace(/\n\n/g, '\n').replace(/1/g, '<div class="square bg-dark"></div>').replace(/0/g, '<div class="square bg-lesslight"></div>').trim().replace(/\n/g, '</br>').replace(/^\t\t/gm, '')
        }
    }
}
</script>

<style scoped>

</style>
