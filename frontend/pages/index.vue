<template>
  <v-row>
    <v-col cols="1">
      <StatusDoughnut />
    </v-col>
    <v-col cols="1">
      <StatusDoughnut />
    </v-col>
    <v-col cols="1">
      <StatusDoughnut />
    </v-col>
    <v-col cols="1">
      <StatusDoughnut />
    </v-col>
    <v-col cols="1">
      <StatusDoughnut />
    </v-col>
    <v-col cols="1">
      <StatusDoughnut />
    </v-col>
  </v-row>
</template>

<script>
import StatusDoughnut from "../components/dashboard/StatusDoughnut";
export default {
  components: {StatusDoughnut},
  methods: {
    test() {
      this.$axios.post('/')
    }
  }
}
</script>
