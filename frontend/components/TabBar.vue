<template>
  <v-app-bar app flat class="px-0" color="#27272f">
    <v-img
      class="mr-5"
      src="logo.png"
      height="40"
      width="40"
      style="filter: grayscale(100%)"
    />
    <v-tabs>
      <v-tab v-for="link in links" :to="link.to" nuxt :ripple="false">
        <v-icon
          v-text="link.icon"
          large
          class="mx-auto"
          :color="link.to === $route.path ? '#ffffff' : '#84848a'"
        />
        <v-slide-x-transition>
          <div
            v-if="link.to === $route.path"
            v-text="link.label"
            class="body-1"
          />
        </v-slide-x-transition>
      </v-tab>
    </v-tabs>
  </v-app-bar>
</template>

<script>
export default {
  name: 'TabBar',
  data: () => ({
    links: [
      { to: '/', label: 'Dashboard', icon: 'mdi-view-dashboard' },
      //TODO: want to make this into a modal.. but maybe not..
      //TODO: maybe make it a "mdi-graph-outline" or some other icon instead idk
      { to: '/pipelines', label: 'Pipelines', icon: 'mdi-cable-data' },
      { to: '/settings', label: 'Settings', icon: 'mdi-cog' }
    ]
  })
}
</script>
