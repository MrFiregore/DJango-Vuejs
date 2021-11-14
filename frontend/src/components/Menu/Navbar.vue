<template>
  <div>
    <b-navbar fixed="top" toggleable="lg" type="dark" variant="success">
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <menu-item v-for="(r,i) in routes" :key="i" :route="r"></menu-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
    name: 'navbar',
    components: {
        MenuItem: () => import(/* webpackChunkName: "menu-item" */ './MenuItem')
    },
    computed: {
        routes () {
            return this.$router.options.routes
        }
    }
}
</script>

<style>
</style>
