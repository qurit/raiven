<template>
  <v-app dark>

    <NuxtLink to="/">
      Home page
    </NuxtLink>

    {{ error }}

  </v-app>
</template>

<script>
export default {
  layout: 'empty',
  props: {
    error: {
      type: Object,
      default: null
    }
  }
}
</script>
