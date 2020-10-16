<template>
  <v-card width="400" height="300">
    <v-row justify="center">
      <div v-if="!!seriesId">
        <v-card-title> Send Series {{ seriesId }} to a Pipeline </v-card-title>
      </div>
      <div v-else-if="!!studyId">
        <v-card-title> Send Study {{ studyId }} to a Pipeline </v-card-title>
      </div>
      <div v-else-if="!!patientId">
        <v-card-title>
          Send Patient {{ patientId }} to a Pipeline
        </v-card-title>
      </div>
      <div v-else>
        <v-card-title> Send Node {{ nodeId }} to a Pipeline </v-card-title>
      </div>
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
      <v-btn
        class="mt-10"
        @click="sendNode(nodeId, patientId, studyId, seriesId)"
        :disabled="this.isDisabled"
      >
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
  props: ['nodeId', 'patientId', 'studyId', 'seriesId'],
  computed: {
    ...mapState('pipelines', ['pipelines']),
    isDisabled: function() {
      return !this.selectedPipelineId
    }
  },
  created() {
    this.$store.dispatch('pipelines/fetchPipelines')
  },
  methods: {
    async sendNode(nodeId, patientId, studyId, seriesId) {
      if (!!seriesId) {
        const res = await axios.put(
          `http://localhost:5000/dicom/node/${nodeId}/${patientId}/${studyId}/${seriesId}`,
          { pipeline_id: this.selectedPipelineId }
        )
        console.log(res.data)
      } else if (!!studyId) {
        const res = await axios.put(
          `http://localhost:5000/dicom/node/${nodeId}/${patientId}/${studyId}`,
          { pipeline_id: this.selectedPipelineId }
        )
        console.log(res.data)
      } else if (!!patientId) {
        const res = await axios.put(
          `http://localhost:5000/dicom/node/${nodeId}/${patientId}`,
          { pipeline_id: this.selectedPipelineId }
        )
        console.log(res.data)
      } else {
        const res = await axios.put(
          `http://localhost:5000/dicom/node/${nodeId}`,
          { pipeline_id: this.selectedPipelineId }
        )
        console.log(res.data)
      }
    }
  }
}
</script>
