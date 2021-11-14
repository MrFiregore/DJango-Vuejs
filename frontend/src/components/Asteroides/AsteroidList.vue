<template>
  <b-container >
    <b-row>
        <b-col class="tex-left">
            <h2 class="text-center">Asteroids List</h2>
            <Asteroids></Asteroids>
        </b-col>
    </b-row>
  </b-container>
</template>

<script>
import messagesService from '@/services/messagesService'
import Asteroids from '@/components/Asteroides/Asteroids'

export default {
    name: 'AsteroidList',
    components: { Asteroids },
    beforeMount () {
        messagesService.fetchSighting()
    }
}
</script>

<style scoped>

</style>
