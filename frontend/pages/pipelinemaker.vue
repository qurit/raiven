<template>
  <div>
    <!-- <v-row justify="start">
      <v-col cols="2">
        <StatusDoughnut />
      </v-col>
      <v-col>
        <TestSocket />
      </v-col>
    </v-row> -->
    <v-row>
      <v-col cols="6">
        <Pipeline />
      </v-col>
      <v-col cols="6">
        <ContainerList />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import StatusDoughnut from '../components/dashboard/StatusDoughnut'
import ContainerList from '../components/ContainerList'
import TestSocket from '../components/TestSocket'
import Pipeline from '../components/Pipeline'
export default {
  components: { Pipeline, TestSocket, ContainerList, StatusDoughnut },
  methods: {
    test() {
      this.$axios.post('/')
    }
  }
}
</script>

