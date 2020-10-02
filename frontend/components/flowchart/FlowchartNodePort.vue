<template>
   <v-hover v-slot:default="{ hover }">
     <v-icon
       small
       :color="hover ? 'red' : 'purple'" v-text="'mdi-circle'"
       @mouseup="$emit('mouseup')"
       @mousedown="$emit('mousedown')"
     />
   </v-hover>
</template>

<script>
export default {
  name: "FlowchartNodePort",
}
</script>
