<template>
  <v-navigation-drawer :app="app" permanent width="125" bottom>
    <n-link to="/login" style="text-decoration: none">
      <v-img
        class="mx-auto mt-8"
        :src="require('@/static/raiven-logo.svg')"
        height="100"
        width="100"
      />
      <div
        class="title text-center nav-title"
        style="font-family: 'Monoton', sans-serif !important; color: white"
      >
        R<span>A</span><span>I</span>VEN
      </div>
    </n-link>
    <v-list class="mt-16" flat>
      <v-list-item
        v-for="link in links"
        :to="link.to"
        nuxt
        class="py-2"
        :ripple="false"
      >
        <v-row justify="center">
          <v-col cols="12" class="text-center">
            <v-icon
              v-text="link.icon"
              large
              class="mx-auto"
              :color="link.to === $route.path ? 'white' : '#84848a'"
            />
            <v-expand-transition>
              <div
                v-if="link.to === $route.path"
                v-text="link.label"
                class="body-1"
              />
            </v-expand-transition>
          </v-col>
        </v-row>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'NavDrawer',
  props: {
    app: Boolean
  },
  data: () => ({
    links: [
      { to: '/', label: 'Dashboard', icon: 'mdi-view-dashboard' },
      { to: '/containers', label: 'Container', icon: 'mdi-toy-brick' },
      {
        to: '/pipeline',
        label: 'Pipelines',
        icon: 'mdi-transit-connection-variant'
      },
      { to: '/settings', label: 'Account', icon: 'mdi-account' }
    ]
  })
}
</script>

<style lang="scss">
.nav-title {
  color: white;
  text-decoration: none;
}
.nav-title > span {
  color: var(--v-primary-base);
}
</style>
