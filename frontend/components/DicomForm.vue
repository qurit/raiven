<template>
  <v-card width="400" height="300">
    <v-row justify="center">
      <v-card-title> Send Node {{ nodeId }} to Pipeline </v-card-title>

      <v-select
        v-model="selectedPipelineId"
        :items="pipelines"
        item-text="name"
        item-value="id"
        label="Choose a pipeline"
        class="ma-8"
      >
      </v-select>
      {{ select }}

      <v-btn class="mt-10" @click="sendNode(nodeId)">
        Send to Pipeline
      </v-btn>
    </v-row>
  </v-card>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  data: () => {
    return {
      selectedPipelineId: null
    }
  },
  props: ['nodeId'],
  computed: {
    ...mapState('pipelines', ['pipelines'])
  },
  created() {
    this.$store.dispatch('pipelines/fetchPipelines')
  },
  methods: {
    async sendNode(nodeId) {
      this.dialog = true
      this.nodeId = nodeId
      const res = await axios.put(
        `http://localhost:5000/dicom/node/${nodeId}`,
        { pipeline_id: this.selectedPipelineId }
      )
      console.log(res.data)
    }
  }
}
</script>
