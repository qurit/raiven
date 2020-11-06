<template>
  <div>
    {{ dicom_series_counts }}
    <v-row>
      <Counters :number="this.patientCount" name="Patients" />

      <Counters :number="this.studyCount" name="Studies" />

      <Counters :number="this.seriesCount" name="Series" />
      <Counters :number="this.pipelineCount" name="Pipelines" />
      <Counters :number="this.containerCount" name="Containers" />
    </v-row>
  </div>
</template>

<script>
import Counters from './Counters'
import { generic_get } from '~/api'

export default {
  name: 'App',
  components: {
    Counters
  },
  data: () => ({
    pipelineCount: 0,
    containerCount: 0,
    patientCount: 0,
    studyCount: 0,
    seriesCount: 0
  }),
  async created() {
    this.getDicomStats()
    this.getPipelineStats()
    this.getContainerStats()
  },
  methods: {
    async getDicomStats() {
      const URL = '/dicom/stats'
      const {
        dicom_patient_counts,
        dicom_series_counts,
        dicom_study_counts
      } = await generic_get(this, URL)
      this.patientCount = dicom_patient_counts
      this.studyCount = dicom_study_counts
      this.seriesCount = dicom_series_counts
    },
    async getPipelineStats() {
      const URL = '/pipeline/stats'
      const { pipeline_counts } = await generic_get(this, URL)
      console.log(pipeline_counts)
      this.pipelineCount = pipeline_counts
    },
    async getContainerStats() {
      const URL = '/container/stats'
      const { container_counts } = await generic_get(this, URL)
      this.containerCount = container_counts
    }
  }
}
</script>
