<template>
  <v-card>
    <v-card-title>
      Your pipelines
    </v-card-title>
    <v-flex v-for="pipeline in pipelines" :key="pipeline.id">
      {{ pipeline.id }}
      {{ pipeline.containerList }}
      <v-btn>
        Edit
      </v-btn>
      <v-btn>
        Remove
      </v-btn>
    </v-flex>
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
    addPipelineContainer() {
      this.containersToList.push({ id: 4, text: 'blah' })
    }
  }
}
</script>
