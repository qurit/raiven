<template>
  <v-card elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title> <b> About this Pipeline</b></v-toolbar-title>
    </v-toolbar>
    <v-row class="ma-4">
      <v-col cols="11"> Pipeline ID: {{ pipelineId }} </v-col>
      {{ editState }}
      <v-icon-btn
        color="icon"
        @click="editState ? saveChanges() : makeEditable()"
        :icon="editState ? 'mdi-content-save' : 'mdi-pencil'"
      ></v-icon-btn>
      <v-col cols="8">
        Pipeline Name:<v-text-field
          solo
          :disabled="!editState"
          v-model="this.pipelineName"
        ></v-text-field>
        <!-- AE title:<v-text-field solo v-model="this.aeTitle"></v-text-field> -->
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { generic_get } from '~/api'
import vIconBtn from './global/v-icon-btn.vue'
export default {
  components: { vIconBtn },
  props: {
    pipelineId: {
      type: String
    }
  },
  data() {
    return {
      pipelineName: '',
      pipelineAETitle: '',
      editState: false
    }
  },
  methods: {
    saveChanges() {
      console.log('ok')
      this.editState = false
    },
    makeEditable() {
      this.editState = true
    },
    async getPipelineInfo() {
      const URL = `/pipeline/${parseInt(this.pipelineId)}`
      // TODO: wait for other PRs to be approved
      // const {name, aeTitle }= await generic_get(this, URL)
      const { name } = await generic_get(this, URL)
      this.pipelineName = name
    }
  },
  mounted() {
    console.log('in created')
    this.getPipelineInfo()
  }
}
</script>
