<template>
  <div>
    <v-row justify="start">
      <v-col cols="2">
        <StatusDoughnut />
      </v-col>
      <v-col>
        <TestSocket />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <TaskCRUD />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import StatusDoughnut from "../components/dashboard/StatusDoughnut";
import TaskCRUD from "../components/TaskCRUD";
import TestSocket from "../components/TestSocket";
export default {
  components: {TestSocket, TaskCRUD, StatusDoughnut},
  methods: {
    test() {
      this.$axios.post('/')
    }
  }
}
</script>
