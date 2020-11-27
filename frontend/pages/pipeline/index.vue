<template>
  <v-row>
    <v-col sm="12" md="7">
      <PipelineList />
    </v-col>
    <v-col sm="12" md="5">
      <SharedPipelineList />
    </v-col>
  </v-row>
</template>

<script>
import { PipelineList, SharedPipelineList } from '~/components/pipeline'
export default {
  components: {
    PipelineList,
    SharedPipelineList
  }
}
</script>
