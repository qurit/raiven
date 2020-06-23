<template>
  <v-app>

    <NavDrawer app />
    <Toast />

    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>

  </v-app>
</template>
<script>
  import NavDrawer from "../components/NavDrawer";
  import Toast from "../components/generic/Toast";
  export default {
    components: {Toast, NavDrawer}
  }
</script>
