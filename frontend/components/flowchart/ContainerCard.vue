<template>
  <v-hover v-slot:default="{ hover }">
    <v-card class="title" :elevation="hover ? 12 : 2" rounded>
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
          color="primary"
          small
          outlined
        />
        <v-spacer />
        <!-- Slot to enable adding of custom actions -->
        <slot></slot>
      </v-row>
    </v-card>
  </v-hover>
</template>
<script>
export default {
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
      if (ctx.container.is_input_container) return ['Input']
      if (ctx.container.is_output_container) return ['Output']
      return ctx.container.tags.map(tag => tag.tag_name)
    }
  }
}
</script>
