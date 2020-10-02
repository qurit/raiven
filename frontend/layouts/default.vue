<template>
  <v-app>

    <TabBar v-if="$vuetify.breakpoint.mdAndDown" />
    <NavDrawer v-else app />
    <Toast />

    <v-content>
      <v-container fluid>
        <nuxt />
      </v-container>
    </v-content>

  </v-app>
</template>
<script>
import NavDrawer from "../components/nav/NavDrawer";
import Toast from "../components/generic/Toast";
import TabBar from "../components/nav/TabBar";
export default {
  components: {TabBar, Toast, NavDrawer},
  created() {
    console.log(this.$vuetify.breakpoint)
  }
}
</script>
