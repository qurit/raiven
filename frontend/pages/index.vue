<!--
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
        <MoveForm />
      </v-col>
      <v-col cols="6">
        <TaskCRUD />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import StatusDoughnut from '../components/dashboard/StatusDoughnut'
import TaskCRUD from '../components/TaskCRUD'
import TestSocket from '../components/TestSocket'
import MoveForm from '../components/MoveForm'
export default {
  components: { MoveForm, TestSocket, TaskCRUD, StatusDoughnut },
  methods: {
    test() {
      this.$axios.post('/')
    }
  }
}
</script>
-->

<template>
  <div>
    <v-row>
      <v-col cols="6">
        <!-- <PipelineStatus /> -->
        <!-- <DonutStatus
          ref="skills_chart"
          :chart-data="chartData"
          :options="options"
        >
        </DonutStatus> -->
        <PipelineStatus :pipelines="pipelines" />
      </v-col>
      <v-col cols="6">
        <UserGuide />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import PipelineStatus from '../components/PipelineStatus'
import UserGuide from '../components/UserGuide'
import { pipelines } from 'vuex'

const options = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    animateRotate: false
  }
}
export default {
  name: 'App',
  components: { PipelineStatus, UserGuide },
  data: function() {
    return {
      // TODO:
      // have to put containers in a store that persists with the user
      // also save the user pipeline
      pipelines: this.$store.state.pipelines.pipelines
    }
  }
}
</script>
