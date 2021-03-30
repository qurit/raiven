<template>
  <v-hover v-slot:default="{ hover }">
    <v-icon
      style="z-index:999;"
      small
      :color="hover ? 'purple' : 'green'"
      v-text="'mdi-circle'"
      @mouseup="$emit('mouseup')"
      @mousedown="$emit('mousedown')"
    />
  </v-hover>
</template>

<script>
export default {
  name: 'FlowchartNodePort'
}
</script>
