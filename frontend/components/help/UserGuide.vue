<template>
  <v-row>
    <v-col sm="12" md="6" v-for="c in components">
      <component :is="c" />
    </v-col>
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
  },
  data: () => ({
    components: [CreateContainerGuide, AddContainerGuide, CreatePipelineGuide, RunPipelineGuide]
  })
}
</script>
