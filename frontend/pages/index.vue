<template>
  <div>
    <v-row>
      <!-- <v-col cols="12"> -->
      <!-- Example on how to use the $toaster plugin i wrote (Used to display notifications to the user)  -->
      <!-- <V-btn color="success" flat @click="$toaster.toastSuccess('Hello!')"
          >Click me for a toast</V-btn
        >
        <V-btn color="error" flat @click="$toaster.toastError('Grrrr')"
          >Click me for an error toast</V-btn
        >
        <V-btn
          color="purple"
          flat
          @click="
            $toaster.toastMessage({ content: 'I am purple', color: 'purple' })
          "
          >Click me for a purple toast</V-btn
        > -->
      <!-- </v-col> -->
      <v-col cols="5">
        <PipelineStatus :pipelines="pipelines" />
      </v-col>
      <v-col cols="7">
        <DicomInstances />
      </v-col>
      <v-col cols="6">
        <PipelineHistogram />
      </v-col>
      <v-col cols="6">
        <DicomTrendChart />
      </v-col>
      <v-col cols="7">
        <DicomBreakdown />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import PipelineStatus from '../components/PipelineStatus'
import PipelineHistogram from '../components/graphs/PipelineHistogram'
import DicomBreakdown from '../components/graphs/DicomBreakdown'
import DicomTrendChart from '../components/graphs/DicomTrendChart'
import DicomInstances from '~/components/dicom/DicomInstances'
import { mapState } from 'vuex'

export default {
  name: 'App',
  components: {
    PipelineStatus,
    PipelineHistogram,
    DicomTrendChart,
    DicomInstances,
    DicomBreakdown
  },
  computed: {
    ...mapState('pipelines', ['pipelines'])
  }
}
</script>
