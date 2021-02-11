<template>
  <v-row>
    <v-col sm="12" md="7">
      <PipelineList />
    </v-col>
    <v-col sm="12" md="5">
      <SharedPipelineList />
    </v-col>
    <v-col sm="12" md="7">
      <PipelineConditions />
    </v-col>
  </v-row>
</template>

<script>
import {
  PipelineList,
  SharedPipelineList,
  PipelineConditions
} from '~/components/pipeline'
export default {
  components: {
    PipelineList,
    SharedPipelineList,
    PipelineConditions
  }
}
</script>

<style lang="css" scoped>
.row-pointer >>> tbody tr :hover {
  cursor: pointer;
}
</style>
