<template>
  <v-btn :color="color" icon @click="$emit('click')">
    <v-icon v-text="iconToShow" />
  </v-btn>
</template>

<script>
export default {
  name: "v-icon-btn",
  props: {
    color: {
      type: String,
      default: 'primary'
    },
    icon: {
      type: String,
      default: 'mdi-plus'
    },
    onClick: {
      type: Function,
      default: () => undefined
    },
    plus: Boolean,
    minus: Boolean,
    delete: Boolean,
    edit: Boolean,
    refresh: Boolean,
  },
  computed: {
    iconToShow: (ctx) => {
      if ( ctx.plus ) return 'mdi-plus'
      if ( ctx.minus ) return 'mdi-minus'
      if ( ctx.delete ) return 'mdi-delete'
      if ( ctx.edit ) return 'mdi-edit'
      if ( ctx.refresh ) return 'mdi-refresh'
      return ctx.icon
    }
  }
}
</script>
