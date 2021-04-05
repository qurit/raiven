<template>
  <v-row>
    <v-col
      sm="12"
      md="6"
      v-for="(c, index) in components"
      :key="`component${index}`"
    >
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
  name: 'UserGuide',
  data: () => ({
    components: [
      CreateContainerGuide,
      AddContainerGuide,
      CreatePipelineGuide,
      RunPipelineGuide
    ]
  })
}
</script>
