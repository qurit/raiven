<template>
  <v-card elevation="6">
    <v-card-title>
      Your pipelines
    </v-card-title>
    <v-flex v-for="pipeline in pipelines" :key="pipeline.id" class="mx-2">
      <b>Pipeline Name:</b>
      {{ pipeline.name }}
      <!-- <b>Containers in Pipeline:</b>
      {{ pipeline.pipeline_containers }} -->

      <v-btn @click="viewPipeline(pipeline.id)">
        <!-- TODO: fix the routing stuff properly with Vue probably /pipleine/:id -->
        View
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
    <v-btn class="ma-2" @click="dialog = true">
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
    viewPipeline(pipelineId) {
      this.$router.push({ path: `/pipeline/${pipelineId}` })
    },
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
