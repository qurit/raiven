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
import PipelineStatus from '../components/PipelineStatus'
import PipelineHistogram from '../components/graphs/PipelineHistogram'
import DicomBreakdown from '../components/graphs/DicomBreakdown'
import DicomTrendChart from '../components/graphs/DicomTrendChart'
import PipelineResults from '~/components/PipelineResults'
import DicomInstances from '~/components/dicom/DicomInstances'
import CounterList from '~/components/CounterList'
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
