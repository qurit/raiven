<template>
  <v-app-bar app flat class="px-0" color="#27272f">
    <v-img class="mr-5" src="raiven-logo.svg" height="40" width="40" />
    <v-tabs>
      <v-tab v-for="link in items" :to="link.to" nuxt :ripple="false">
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
  props: {
    items: {
      type: Array,
      default: () => [
        {to: '/', label: 'Dashboard', icon: 'mdi-chart-box-outline'}
      ]
    }
  }
}
</script>
