import axios from 'axios'

axios.defaults.port = 8000

export default axios.create({
    baseURL: '/api',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
})
