<template>
  <v-row>
    <v-col sm="12" md="7">
      <PipelineList />
    </v-col>
  </v-row>
</template>

<script>
import PipelineList from '~/components/pipeline/PipelineList'
export default {
  components: {
    PipelineList
  }
}
</script>
