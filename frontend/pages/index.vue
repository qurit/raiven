<template>
  <v-row>
    <v-col cols="4">
      <StatusDoughnut />
    </v-col>
    <v-col cols="6">
      <TaskCRUD />
    </v-col>
  </v-row>
</template>

<script>
import StatusDoughnut from "../components/dashboard/StatusDoughnut";
import TaskCRUD from "../components/TaskCRUD";
export default {
  components: {TaskCRUD, StatusDoughnut},
  methods: {
    test() {
      this.$axios.post('/')
    }
  }
}
</script>
