<template>
  <b-nav-item :to="{name: route.name}" :active='$route.name == route.name'>{{name}}</b-nav-item>
</template>

<script>
export default {
    name: 'menu-item',
    props: {
        route: {
            type: Object
        }
    },
    computed: {
        name () {
            return this.route.name.replace(/([A-Z])/g, ' $1').trim()
        }
    }
}
</script>
