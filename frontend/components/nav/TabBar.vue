<template>
  <v-app-bar app flat class="px-0" color="#27272f">
    <n-link to="/" style="text-decoration: none">
      <v-img
        class="mr-5"
        :src="require('@/static/raiven-logo.svg')"
        height="40"
        width="40"
      />
    </n-link>
    <v-tab v-for="link in items" :to="link.to" nuxt :ripple="false" :key="link.to">
      <v-icon
        v-text="link.icon"
        large
        class="mx-auto"
        :color="link.to === $route.path ? 'icon' : '#84848a'"
      />
    </v-tab>
    <v-btn color="primary" dark icon @click="$auth.logout('local')">
      <v-icon>mdi-power-standby</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'TabBar',
  props: {
    items: {
      type: Array,
      default: () => [
        { to: '/', label: 'Dashboard', icon: 'mdi-chart-box-outline' }
      ]
    }
  }
}
</script>
