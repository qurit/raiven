<template>
  <v-row>
    <v-col sm="12" md="6"> <CreateContainerGuide /> </v-col>
    <v-col sm="12" md="6"> <AddContainerGuide /> </v-col>
    <v-col sm="12" md="6"> <CreatePipelineGuide /> </v-col>
    <v-col sm="12" md="6"> <RunPipelineGuide /> </v-col>
  </v-row>
</template>

<script>
import CreateContainerGuide from '~/components/help/CreateContainerGuide'
import AddContainerGuide from '~/components/help/AddContainerGuide'
import CreatePipelineGuide from '~/components/help/CreatePipelineGuide'
import RunPipelineGuide from '~/components/help/RunPipelineGuide'

export default {
  components: {
    CreateContainerGuide,
    AddContainerGuide,
    CreatePipelineGuide,
    RunPipelineGuide
  }
}
</script>
