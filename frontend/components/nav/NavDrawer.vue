<template>
  <v-navigation-drawer :app="app" permanent width="125" bottom>
    <n-link to="/" style="text-decoration: none">
      <v-img
        class="mx-auto mt-8"
        :src="require('@/static/raiven-logo.svg')"
        height="100"
        width="100"
      />
      <div
        class="title text-center nav-title"
        style="font-family: 'Quicksand', cursive !important; color: white"
      >
        R<span>A</span><span>I</span>VEN
      </div>
    </n-link>
    <v-list class="mt-16" flat style="flex: 1">
      <!-- Links -->
      <!-- Links can be changed in the default layout -->
      <v-list-item
        v-for="link in items"
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
              :color="link.to === $route.path ? '' : '#84848a'"
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

    <template v-slot:append>
      <v-col cols="12" class="text-center pb-0">
        <v-tooltip top dark>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              dark
              icon
              v-bind="attrs"
              v-on="on"
              @click="$auth.logout('local')"
            >
              <v-icon>mdi-power-standby</v-icon>
            </v-btn>
          </template>
          <span>Logout</span>
        </v-tooltip>
      </v-col>
      <v-col cols="12" class="text-center">{{ $auth.user.name }}</v-col>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'NavDrawer',
  props: {
    app: Boolean,
    items: {
      type: Array,
      default: () => [
        { to: '/', label: 'Dashboard', icon: 'mdi-chart-box-outline' }
      ]
    }
  }
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
