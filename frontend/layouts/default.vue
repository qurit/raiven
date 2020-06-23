<template>
  <v-app>

    <NavDrawer app />

    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>

  </v-app>
</template>
<script>
  import NavDrawer from "../components/NavDrawer";
  export default {
    components: {NavDrawer}
  }
</script>
