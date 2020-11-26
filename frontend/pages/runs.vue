<template>
  <div>
    <v-row>
      <v-col sm="12" md="3">
        <DicomInstances />
      </v-col>
      <v-col sm="12" md="3">
        <PipelineStatus :pipelines="pipelines" />
      </v-col>
      <v-col sm="12" md="6">
        <PipelineResults />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { PipelineResults, PipelineStatus } from '~/components/pipeline'
import { DicomInstances } from '~/components/dicom'
import { mapState } from 'vuex'

export default {
  components: {
    PipelineStatus,
    DicomInstances,
    PipelineResults
  },
  computed: {
    ...mapState('pipelines', ['pipelines'])
  }
}
</script>
