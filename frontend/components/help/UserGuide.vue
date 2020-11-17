<template>
  <v-row>
    <v-col sm="12" md="6"> <CreateContainerGuide /> </v-col>
    <v-col sm="12" md="6"> <AddContainerGuide /> </v-col>
    <v-col sm="12" md="6"> <CreatePipelineGuide /> </v-col>
    <v-col sm="12" md="6"> <RunPipelineGuide /> </v-col>
  </v-row>
</template>

<script>
import {
  CreateContainerGuide,
  AddContainerGuide,
  CreatePipelineGuide,
  RunPipelineGuide
} from '~/components/help/'

export default {
  components: {
    CreateContainerGuide,
    AddContainerGuide,
    CreatePipelineGuide,
    RunPipelineGuide
  }
}
</script>
