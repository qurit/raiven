<template>
  <div>
    <v-row>
      <v-col cols="12">
        <CounterList />
      </v-col>
      <v-col sm="12" md="4">
        <PipelineStatus :pipelines="pipelines" />
      </v-col>
      <v-col sm="12" md="4">
        <PipelineHistogram />
      </v-col>
      <v-col sm="12" md="4">
        <DicomTrendChart />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { PipelineStatus, PipelineResults } from '~/components/pipeline'
import {
  DicomBreakdown,
  DicomTrendChart,
  PipelineHistogram
} from '~/components/graphs/'
import { DicomInstances } from '~/components/dicom'
import { CounterList } from '~/components/counter'
import { mapState } from 'vuex'

export default {
  name: 'App',
  components: {
    PipelineStatus,
    PipelineHistogram,
    DicomTrendChart,
    DicomInstances,
    DicomBreakdown,
    CounterList,
    PipelineResults
  },
  computed: {
    ...mapState('pipelines', ['pipelines'])
  }
}
</script>
