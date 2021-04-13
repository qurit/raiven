<template>
  <v-card height="50vh" color="#373740">
    <v-card-title>
      Error Message:
    </v-card-title>
    <v-card-text class="my-n10">{{ this.error.stderr }}</v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ErrorInfo',
  props: {
    error: {
      type: Object
    }
  }
}
</script>
