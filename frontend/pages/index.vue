<template>
  <v-row>
    <v-col>PIPELINE</v-col>
    <v-btn @click="test">API</v-btn>
  </v-row>
</template>

<script>
export default {
  methods: {
    test() {
      this.$axios.post('/')
    }
  }
}
</script>
