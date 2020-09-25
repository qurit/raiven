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
    <v-btn @click="addPipelineContainer">
      Save pipeline
    </v-btn>
  </v-card>
</template>

<script>
export default {
  data: function() {
    return {
      // TODO:
      // have to put containers in a store that persists with the user
      // also save the user pipeline
      containers: [
        { id: 1, text: 'Algorithm 1' },
        { id: 2, text: 'Algorithm 2' },
        { id: 3, text: 'Algorithm 3' }
      ],
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
