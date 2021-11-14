import Vue from 'vue'
import Router from 'vue-router'
import AsteroidList from '@/components/Asteroides/AsteroidList'
import SightingList from '@/components/Asteroides/SightingList'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'AsteroidList',
            component: AsteroidList,
            meta: {
                visible: true
            }
        },
        {
            path: '/list_sighting',
            name: 'SightingList',
            component: SightingList,
            meta: {
                visible: true
            }
        }
    ]
})
