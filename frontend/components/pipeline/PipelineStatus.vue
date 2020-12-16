<template>
  <v-card elevation="6" height="460" class="overflow-y-auto overflow-x-hidden">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title> <b>Pipelines in Progress</b></v-toolbar-title>
      <v-spacer />
      <v-btn icon>
        <v-icon @click="this.getPipelineProgress" color="#373740"
          >mdi-refresh</v-icon
        >
      </v-btn>
    </v-toolbar>
    <v-divider light />
    <v-flex v-for="run in this.pipelineRuns" :key="run.id">
      <v-card>
        <v-row justify="left" align="center" class="px-4">
          <v-card-subtitle> Run ID: {{ run.id }} </v-card-subtitle>
          <v-card-subtitle>
            From Pipeline: {{ run.pipeline.name }}
          </v-card-subtitle>
        </v-row>
        <v-row class="mt-n3 ma-2">
          <v-progress-linear
            rounded
            :color="run.status === 'complete' ? 'success' : 'info'"
            buffer-value="0"
            :value="status[run.status]"
            stream
          ></v-progress-linear>
        </v-row>
      </v-card>
    </v-flex>
  </v-card>
</template>

<script>
import { generic_get } from '~/api'

export default {
  name: 'PipelineStatus',
  props: ['pipelines'],
  data() {
    return {
      pipelineRuns: [],
      // TODO: change these statuses
      status: {
        created: 0,
        exited: 20,
        running: 40,
        complete: 100
      }
    }
  },
  methods: {
    async getPipelineProgress() {
      const URL = '/pipeline/results'
      try {
        this.pipelineRuns = await generic_get(this, URL)
      } catch (e) {
        console.log(e)
      }
    }
  },
  created() {
    this.getPipelineProgress()
  }
}
</script>
