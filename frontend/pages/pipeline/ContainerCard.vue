<template>
  <v-hover v-slot:default="{ hover }">
    <v-card class="ma-2 title" :color="hover ? colors.hover : containerColor">
        <v-card-title v-text="container.name"/>
        <v-card-subtitle v-text="`ID: ${container.id}`" />
        <v-card-text>
            {{ container.description }}
        </v-card-text>
        <v-card-actions>
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
            hover: 'green',
            input: 'orange',
            output: 'purple',
            default: 'blue'
        })
      }
  },
  computed: {
    containerColor: ctx => {
      switch (ctx.container) {
        case ctx.is_output_container: return ctx.colors.output
        case ctx.is_input_container: return ctx.colors.input
        default: return ctx.colors.default
      }
    }
  }
}
</script>
