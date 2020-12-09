<template>
  <v-app>
    <TabBar v-if="$vuetify.breakpoint.mdAndDown" :items="links" />
    <NavDrawer v-else app :items="links" />
    <Toast />

    <v-content>
      <v-container fluid>
        <nuxt />
      </v-container>
    </v-content>
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
          icon:
            this.$route.path === '/containers'
              ? 'mdi-package-variant'
              : 'mdi-package-variant-closed'
        },
        {
          to: '/pipeline',
          label: 'Pipelines',
          icon: 'mdi-transit-connection-variant'
        },
        { to: '/runs', label: 'Runs', icon: 'mdi-air-filter' },
        { to: '/help', label: 'Help', icon: 'mdi-help' },
        ...(this.$auth.user.is_admin
          ? [{ to: '/admin', label: 'Admin', icon: 'mdi-head-cog-outline' }]
          : [])
      ]
    }
  },
  created() {
    this.$store.dispatch('fetchConfig')
  }
}
</script>
