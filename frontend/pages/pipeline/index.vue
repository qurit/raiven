<template>
  <v-card>
    *** FULFILLS: As a researcher, I would like to have a dashboard to view the
    status of my pipelines *** *** View all pipelines but the status of running
    ones is on the index dashboard landing page ***
    <v-card-title>
      Your pipelines
    </v-card-title>
    <v-flex v-for="pipeline in pipelines" :key="pipeline.id">
      <b>Pipeline Name:</b>
      {{ pipeline.name }}
      <!-- <b>Containers in Pipeline:</b>
      {{ pipeline.pipeline_containers }} -->

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
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-text-field
          v-model="pipelineName"
          label="Pipeline Name"
          required
          class="pa-15"
        />
        <v-btn @click="dialog = false" class="ma-2"> Close </v-btn>
        <!-- <nuxt-link to="/"> -->
        <v-btn @click="savePipeline">
          Save
        </v-btn>
        <!-- </nuxt-link> -->
      </v-card>
    </v-dialog>
    <v-btn @click="dialog = true">
      <!-- TODO: maybe this routing should be to "/pipeline/:id/edit" or something instead of pipelinemaker (this is for new pipelines)-->
      Add Pipeline
    </v-btn>
  </v-card>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  data: function() {
    return {
      // TODO:
      // have to put containers in a store that persists with the user
      // also save the user pipeline
      dialog: false,
      pipelineName: ''
    }
  },
  methods: {
    removePipeline(pipeline) {
      this.$store.dispatch('pipelines/deletePipeline', pipeline.id)
    },
    savePipeline() {
      const payload = {
        user_id: 1,
        name: this.pipelineName
      }
      const test = this.$store.dispatch('pipelines/addPipeline', payload)
      var new_pipeline_id
      test.then(x => {
        this.$router.push({ path: `/pipeline/${x.data.id}` })
        console.log(x)
      })
      console.log(new_pipeline_id)
      this.dialog = false
    }
  },
  computed: {
    ...mapState('pipelines', ['pipelines'])
  },
  created() {
    this.$store.dispatch('pipelines/fetchPipelines')
  }
}
</script>
