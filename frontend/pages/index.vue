<template>
  <v-row>
    <v-col cols="6">
      <v-card>
        <v-card-title>AETS</v-card-title>
        <v-divider />
        sdj
      </v-card>
    </v-col>
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
