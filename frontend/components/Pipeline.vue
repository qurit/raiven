<template>
  <v-card>
    <v-card-title>
      Build Your Pipeline
    </v-card-title>
    <v-flex>
      <v-select
        v-for="container in containersToList"
        :key="container.id"
        :items="containers"
        label="Choose your container"
        item-text="title"
        background-color="red"
        solo
        flat
        dense
        single-line
      >
        <v-btn>
          Remove container
        </v-btn>
      </v-select>
    </v-flex>
    <v-btn @click="addPipelineContainer">
      Add to pipeline
    </v-btn>
    <!-- TODO: add route to save the pipeline to the user -->
    <v-btn @click="addPipelineContainer">
      Save pipeline
    </v-btn>
  </v-card>
</template>

<script>
import { containers } from 'vuex'

export default {
  data: function() {
    return {
      // TODO:
      // have to put containers in a store that persists with the user
      // also save the user pipeline
      containers: this.$store.state.containers.containers,
      containersToList: [
        { id: 1, text: 'Testing 1' },
        { id: 2, text: 'Testing 2' },
        { id: 3, text: 'Testing 3' }
      ]
    }
  },
  methods: {
    addPipelineContainer() {
      this.containersToList.push({ id: 4, text: 'blah' })
    }
  }
}
</script>
