<template>
  <v-app>
    <TabBar v-if="$vuetify.breakpoint.mdAndDown" :items="links" />
    <NavDrawer v-else app :items="links" />
    <Toast />

    <v-main>
      <v-container fluid>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
import { NavDrawer, TabBar } from '~/components/nav'
import Toast from '~/components/generic/Toast'

export default {
  components: { TabBar, Toast, NavDrawer },
  computed: {
    links() {
      return [
        { to: '/', label: 'Dashboard', icon: 'mdi-chart-box-outline' },
        {
          to: '/containers',
          label: 'Containers',
          icon: this.$route.path === '/containers'
            ? 'mdi-package-variant'
            : 'mdi-package-variant-closed'
        },
        {
          to: '/pipeline',
          label: 'Pipelines',
          icon: this.$route.path === '/pipeline'
            ? 'mdi-transit-connection-variant'
            : 'mdi-transit-connection-horizontal'
        },
        {
          to: '/runs', label: 'Runs',
          icon: this.$route.path === '/runs'
            ? 'mdi-play'
            : 'mdi-play-outline'
        },
        {
          to: '/settings',
          label: 'Settings',
          icon: this.$route.path === '/settings'
              ? 'mdi-account-cog'
              : 'mdi-account-cog-outline'
        },
        {
          to: '/help',
          label: 'Help',
          icon: 'mdi-help'
        },
        ...(
          this.$auth.user.is_admin ? [
          {
            to: '/admin',
            label: 'Admin',
            icon: this.$route.path === '/admin'
              ? 'mdi-head-cog'
              : 'mdi-head-cog-outline'
          }] : [])
      ]
    }
  },
  created() {
    this.$store.dispatch('fetchConfig')
  }
}
</script>
