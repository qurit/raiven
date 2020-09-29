<template>
  <v-card>
    *** FULFILLS: As a researcher, I would like to have a dashboard to view the
    status of my pipelines *** *** View all pipelines but the status of running
    ones is on the index dashboard landing page ***
    <v-card-title>
      Your pipelines
    </v-card-title>
    <v-flex v-for="pipeline in pipelines" :key="pipeline.id">
      <b>Pipeline Title:</b>
      {{ pipeline.title }}
      <b>Containers in Pipeline:</b>
      {{ pipeline.containerList }}
      <b>Running status: </b>
      {{ pipeline.status }}
      <v-btn>
        <!-- TODO: fix the routing stuff properly with Vue probably /pipleine/:id -->
        <nuxt-link to="/pipeline/1">
          View
        </nuxt-link>
      </v-btn>
      <v-btn @click="removePipeline(pipeline)">
        Remove
      </v-btn>
    </v-flex>
    <v-btn>
      <!-- TODO: maybe this routing should be to "/pipeline/:id/edit" or something instead of pipelinemaker (this is for new pipelines)-->
      <nuxt-link to="/pipelinemaker">
        Add
      </nuxt-link>
    </v-btn>
  </v-card>
</template>

<script>
import { pipelines } from 'vuex'

export default {
  data: function() {
    return {
      // TODO:
      // have to put containers in a store that persists with the user
      // also save the user pipeline
      pipelines: this.$store.state.pipelines.pipelines
    }
  },
  methods: {
    removePipeline(pipeline) {
      this.$store.commit('pipelines/delete', pipeline)
    }
  }
}
</script>
