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
        style="font-family: 'Monoton', sans-serif !important; color: white"
      >
        R<span>A</span><span>I</span>VEN
      </div>
    </n-link>
    <v-list
      class="mt-16"
      flat
      style="flex: 1,  flexDirection: 'column', justifyContent: 'space-between' "
    >
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
    <v-row justify="center" align="center" class="pt-8">
      <v-col cols="12" class="text-center">
        <v-icon-btn
          large
          color="cancel"
          @click="dialog = true"
          icon="mdi-power-standby"
        />
      </v-col>
      <v-col cols="12" class="text-center">
        {{ $auth.user.name }}
      </v-col>
    </v-row>
    <div v-if="dialog">
      <v-dialog v-model="dialog" width="500px" height="600px">
        <LogoutConfirmation @cancel="dialog = false" />
      </v-dialog>
    </div>
  </v-navigation-drawer>
</template>

<script>
import VIconBtn from '~/components/global/v-icon-btn'
import LogoutConfirmation from '~/components/LogoutConfirmation'

export default {
  name: 'NavDrawer',
  components: {
    VIconBtn,
    LogoutConfirmation
  },
  props: {
    app: Boolean
  },
  data: () => ({
    dialog: false,
    links: [
      { to: '/', label: 'Dashboard', icon: 'mdi-chart-box-outline' },
      { to: '/containers', label: 'Container', icon: 'mdi-toy-brick' },
      {
        to: '/pipeline',
        label: 'Pipelines',
        icon: 'mdi-transit-connection-variant'
      },
      { to: '/runs', label: 'Runs', icon: 'mdi-cogs' },
      { to: '/help', label: 'Help', icon: 'mdi-help' }
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
