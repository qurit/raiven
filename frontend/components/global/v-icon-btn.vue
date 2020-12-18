<template>
  <v-btn :color="color" icon @click="$emit('click')" :to="to">
    <v-icon v-text="iconToShow" :large="large" />
  </v-btn>
</template>

<script>
export default {
  name: 'v-icon-btn',
  props: {
    color: {
      type: String,
      default: 'primary'
    },
    to: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: 'mdi-plus'
    },
    onClick: {
      type: Function,
      default: () => undefined
    },
    large: Boolean,
    plus: Boolean,
    minus: Boolean,
    back: Boolean,
    save: Boolean,
    delete: Boolean,
    edit: Boolean,
    refresh: Boolean,
    close: Boolean,
    info: Boolean
  },
  computed: {
    iconToShow: ctx => {
      if (ctx.plus) return 'mdi-plus'
      if (ctx.minus) return 'mdi-minus'
      if (ctx.delete) return 'mdi-delete'
      if (ctx.edit) return 'mdi-edit'
      if (ctx.save) return 'mdi-content-save'
      if (ctx.refresh) return 'mdi-refresh'
      if (ctx.back) return 'mdi-arrow-left'
      if (ctx.close) return 'mdi-close'
      if (ctx.info) return 'mdi-information-outline'
      return ctx.icon
    }
  }
}
</script>
