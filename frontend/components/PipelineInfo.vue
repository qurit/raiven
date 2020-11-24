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
          v-model="pipelineName"
        ></v-text-field>

        <!-- AE title:<v-text-field solo v-model="this.aeTitle"></v-text-field> -->
      </v-col>

      <!-- <v-col cols="12">
        Results from this Pipeline
        <PipelineResults :pipelineId="this.pipelineId" />
      </v-col> -->
      <v-col cols="12">
        More Info
        <PipelineFullInfo :pipelineId="this.pipelineId" />
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { generic_get, generic_put } from '~/api'
import vIconBtn from './global/v-icon-btn.vue'
import PipelineFullInfo from './PipelineFullInfo'
import PipelineResults from './PipelineResults'
export default {
  components: { vIconBtn, PipelineResults, PipelineFullInfo },
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
    async saveChanges() {
      try {
        const URL = `/pipeline/${this.pipelineId}/edit`
        const payload = {
          name: this.pipelineName
          // aeTitle: this.pipelineAETitle
        }
        await generic_put(this, URL, payload)
        this.editState = false
        this.$toaster.toastSuccess('Changes saved!')
      } catch (e) {
        this.$toaster.toastError('Could not save changes')
      }
    },
    makeEditable() {
      this.editState = true
    },
    getPipelineInfo() {
      this.getPipelineName()
      this.getPipelineErrors()
    },
    async getPipelineName() {
      // get Pipeline Name and AE Title
      const URL = `/pipeline/${this.pipelineId}`
      // TODO: wait for other PRs to be approved
      // const {name, aeTitle }= await generic_get(this, URL)
      const { name } = await generic_get(this, URL)
      this.pipelineName = name
      console.log(this.pipelineName)
    },
    async getPipelineErrors() {
      // get Pipeline Errors
      console.log('in errors')
    }
  },
  created() {
    console.log('in created')
    this.getPipelineInfo()
  }
}
</script>
