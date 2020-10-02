<template>
  <v-card>
    *** IN PROGRESS: As a researcher, I would like to be able to create Imaging
    pipelines by linking predefined components together *** *** CHANGE TO DRAG
    AND DROP *** and *** As a researcher, I would like to save the pipelines I
    have created ***
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
        background-color="#045D56"
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
      Add Container to Pipeline
    </v-btn>
    <!-- TODO: add route to save the pipeline to the user -->
    <v-btn color="primary">
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
