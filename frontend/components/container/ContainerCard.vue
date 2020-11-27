<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="title"
      :elevation="hover ? 12 : 4"
      style="transition: background-color 0.2s ease-out"
      rounded
    >
      <v-card-title v-text="container.name" />
      <v-card-subtitle v-text="`ID: ${container.id}`" class="pb-4" />
        {{ container.description }}
      </v-card-subtitle>
      <v-row justify="center" v-if="container.user_id !== $auth.user.id">
        <v-chip v-text="'From: ' + container.user.name" color="info" />
      </v-row>
      <v-card-actions class="mt-n5">
        <v-chip
          v-for="chip in chips"
          v-text="chip"
          class="mr-1"
          :color="containerColor"
        />
        <v-spacer />
        <!-- Slot to enable adding of custom actions -->
        <slot></slot>
      </v-card-actions>
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
        input: 'orange',
        output: 'purple',
        default: 'blue'
      })
    }
  },
  computed: {
    containerColor: ctx => {
      if (ctx.container.is_output_container) return ctx.colors.output
      else if (ctx.container.is_input_container) return ctx.colors.input
      else return ctx.colors.default
    },
    chips: ctx => {
      const chips = []
      if (ctx.container.is_output_container) chips.push('Output')
      if (ctx.container.is_input_container) chips.push('Input')
      return chips
    }
  }
}
</script>
