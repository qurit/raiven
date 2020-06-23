<template>
  <v-btn :color="color" icon small @click="$emit('click')">
    <v-icon v-text="icon" />
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
    }
  }
}
</script>
