<template>
  <div>
    *** FULFILLS: As a researcher, I would like to have a dashboard to view the
    status of my pipelines ***
    <v-card-title>
      Your pipelines in progress
    </v-card-title>
    <div v-if="pipelines.length > 0">
      <v-flex v-for="pipeline in pipelines" :key="pipeline.id">
        <v-card>
          <v-card-subtitle>
            {{ pipeline.title }}
          </v-card-subtitle>
          <v-flex>
            <v-progress-linear
              color="light-blue"
              buffer-value="0"
              :value="pipeline.status"
              stream
            ></v-progress-linear>
            <v-btn color="error">
              Stop
            </v-btn>
          </v-flex>
        </v-card>
      </v-flex>
    </div>
    <div v-else>
      <v-row>
        You have no pipelines running. Click "Add a Pipeline" to customize a
        pipeline to run or "View Pipelines" to choose a pipeline to run.
        <v-btn>
          <nuxt-link to="/pipelinemaker">
            Add a Pipeline
          </nuxt-link>
        </v-btn>
        <v-btn>
          <nuxt-link to="/pipeline">
            View Pipelines
          </nuxt-link>
        </v-btn>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PipelineStatus',
  props: ['pipelines']
  // can do prop validation
  // props: {
  //   pipelines: {
  //     type: Array,
  //     required: true
  //   }
  // }
}
</script>
