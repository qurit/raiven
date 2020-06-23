<template>
  <v-navigation-drawer :app="app" permanent width="150">
    <v-img class="mx-auto mt-8"  src="logo.png" height="100" width="100" style="filter: grayscale(100%)"/>

    <v-list class="mt-16">
      <v-list-item v-for="link in links" :to="link.to" nuxt class="py-4">
        <v-row justify="center">
          <v-col cols="12" class="text-center">
            <v-icon v-text="link.icon" large class="mx-auto" :color="link.to === $route.path ? '#ffffff' : '#84848a'"/>
            <v-expand-transition>
              <div v-if="link.to === $route.path" v-text="link.label" class="body-1"/>
            </v-expand-transition>
          </v-col>
        </v-row>
      </v-list-item>
    </v-list>

  </v-navigation-drawer>
</template>

<script>
export default {
  name: "NavDrawer",
  props: {
    app: Boolean
  },
  data: () => ({
    links: [
      { to: '/', label: 'Dashboard', icon: 'mdi-view-dashboard'},
      { to: '/settings', label: 'Settings', icon: 'mdi-cog'}
    ]
  })
}
</script>

<style scoped>

</style>
