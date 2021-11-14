import api from '@/services/api'

export default {
    fetchAsteroids () {
        return api.get('asteroid').then(response => response.data.data)
    },
    fetchSighting () {
        return api.get('sighting').then(response => response.data.data)
    }
}
