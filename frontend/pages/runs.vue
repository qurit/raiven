<template>
  <div>
    <v-row>
      <v-col sm="12" md="3">
        <PipelineStatus />
      </v-col>
      <v-col sm="12" md="3">
        <DicomInstances />
      </v-col>
      <v-col sm="12" md="6">
        <PipelineResults />
      </v-col>
      <v-col sm="12" md="6">
        <VirtualFileSystem />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import {
  PipelineResults,
  PipelineStatus,
  VirtualFileSystem
} from '~/components/pipeline'
import { DicomInstances } from '~/components/dicom'
import { mapState } from 'vuex'
export default {
  components: {
    PipelineStatus,
    DicomInstances,
    PipelineResults,
    VirtualFileSystem
  },
  computed: {
    ...mapState('pipelines', ['pipelines'])
  }
}
</script>
