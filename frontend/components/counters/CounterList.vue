<template>
  <div>
    <v-row justify="space-between" no-gutters>
      <CounterCard :number="this.containerCount" name="Containers" />
      <CounterCard :number="this.pipelineCount" name="Pipelines" />
      <CounterCard :number="this.pipelineRunCount" name="Pipeline Runs" />
      <CounterCard :number="this.patientCount" name="Patients" />
      <CounterCard :number="this.studyCount" name="Studies" />
      <CounterCard :number="this.seriesCount" name="Series" />
    </v-row>
  </div>
</template>

<script>
import CounterCard from './CounterCard'
import { generic_get } from '~/api'

export default {
  name: 'App',
  components: {
    CounterCard
  },
  data: () => ({
    pipelineCount: 0,
    pipelineRunCount: 0,
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
      const { pipeline_counts, pipeline_run_counts } = await generic_get(
        this,
        URL
      )
      this.pipelineCount = pipeline_counts
      this.pipelineRunCount = pipeline_run_counts
    },
    async getContainerStats() {
      const URL = '/container/stats'
      const { container_counts } = await generic_get(this, URL)
      this.containerCount = container_counts
    }
  }
}
</script>
