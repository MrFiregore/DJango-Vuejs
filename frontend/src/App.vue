<template>
  <div>
    <navbar></navbar>
    <b-container fluid>
      <b-row class="min-vh-100">
        <b-col>
          <router-view></router-view>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>

export default {
    name: 'App',
    components: {
        Navbar: () => import('./components/Menu/Navbar')
    }

}
</script>

<style lang="scss">
  @import "assets/scss/custom";

</style>
