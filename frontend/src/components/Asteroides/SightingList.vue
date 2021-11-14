<template>
  <b-container >
    <b-row>
      <b-col class="tex-left">
        <h2 class="text-center">Sightings list</h2>
          <Sighting></Sighting>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import messagesService from '@/services/messagesService'
import Sighting from '@/components/Asteroides/Sighting'

export default {
    name: 'SightingList',
    components: { Sighting },
    beforeMount () {
        messagesService.fetchSighting()
    }
}
</script>

<style scoped>

</style>
