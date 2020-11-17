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
import { PipelineStatus } from '~/components/pipeline'
import { CounterList } from '~/components/counters'
import { DicomTrendChart, PipelineHistogram } from '~/components/graphs'

import { mapState } from 'vuex'

export default {
  name: 'App',
  components: {
    PipelineStatus,
    PipelineHistogram,
    DicomTrendChart,
    CounterList
  },
  computed: {
    ...mapState('pipelines', ['pipelines'])
  }
}
</script>
