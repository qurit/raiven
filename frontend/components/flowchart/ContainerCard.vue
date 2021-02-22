<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="title"
      :elevation="hover ? 12 : 2"
      style="transition: background-color 0.2s ease-out"
      rounded
    >
      <v-card-title v-text="container.name" />
      <v-card-subtitle>
        {{ container.description }}
      </v-card-subtitle>
      <v-row justify="center" v-if="container.user_id !== $auth.user.id">
        <v-chip
          class="mb-1"
          v-text="'From: ' + container.user.name"
          color="info"
        />
      </v-row>
      <v-row class="ma-1">
        <v-chip
          v-for="chip in chips"
          v-text="chip"
          class="mr-1 mb-1"
          color="confirm"
        />
        <v-spacer />
        <!-- Slot to enable adding of custom actions -->
        <slot></slot>
      </v-row>
    </v-card>
  </v-hover>
</template>
<script>
import vIconBtn from '../global/v-icon-btn.vue'
export default {
  components: { vIconBtn },
  name: 'ContainerCard',
  props: {
    container: {
      type: Object,
      default: () => undefined
    },
    colors: {
      type: Object,
      default: () => ({
        default: 'blue',
        tag: 'green'
      })
    }
  },
  computed: {
    chips: ctx => {
      if (!!ctx.container.tags) {
        const chips = ctx.container.tags.split(',')
        return chips
      }
    }
  }
}
</script>
