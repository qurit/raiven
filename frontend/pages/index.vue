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
import PipelineStatus from '../components/runs/PipelineStatus'
import PipelineResults from '~/components/runs/PipelineResults'
import DicomInstances from '~/components/runs/DicomInstances'
import CounterList from '~/components/CounterList'
import { mapState } from 'vuex'

import {
  DicomBreakdown,
  DicomTrendChart,
  PipelineHistogram
} from '~/components/graphs'

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
