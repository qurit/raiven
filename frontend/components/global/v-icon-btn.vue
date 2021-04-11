<template>
  <!-- <v-btn
    :disabled="disabled"
    :color="color"
    icon
    @click="$emit('click')"
    :to="to"
  > -->
  <v-btn :disabled="disabled" :color="color" icon @click="hello" :to="to">
    <v-icon v-text="iconToShow" :large="large" />
  </v-btn>
</template>

<script>
export default {
  name: 'v-icon-btn',
  props: {
    disabled: {
      type: Boolean,
      default: false
    },
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
    // onClick: {
    //   type: Function,
    //   default: () => undefined
    // },
    large: Boolean,
    plus: Boolean,
    minus: Boolean,
    back: Boolean,
    save: Boolean,
    delete: Boolean,
    deleteEmpty: Boolean,
    edit: Boolean,
    refresh: Boolean,
    close: Boolean
  },
  methods: {
    hello() {
      console.log(this.icon)
    }
  },
  computed: {
    iconToShow: ctx => {
      if (ctx.plus || ctx.icon === 'plus') return 'mdi-plus'
      if (ctx.minus || ctx.icon === 'minus') return 'mdi-minus'
      if (ctx.delete || ctx.icon === 'delete') return 'mdi-delete'
      if (ctx.deleteEmpty || ctx.icon === 'deleteEmpty')
        return 'mdi-delete-empty'
      if (ctx.edit || ctx.icon === 'edit') return 'mdi-edit'
      if (ctx.save || ctx.icon === 'save') return 'mdi-content-save'
      if (ctx.refresh || ctx.icon === 'refresh') return 'mdi-refresh'
      if (ctx.back || ctx.icon === 'back') return 'mdi-arrow-left'
      if (ctx.close || ctx.icon === 'close') return 'mdi-close'
      return ctx.icon
    }
  }
}
</script>
