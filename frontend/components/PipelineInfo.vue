<template>
  <v-card elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title> <b> About this Pipeline</b></v-toolbar-title>
    </v-toolbar>
    <v-row class="ma-4">
      <v-col cols="11"> Pipeline ID: {{ pipelineId }} </v-col>
      <v-icon-btn
        color="icon"
        @click="editState ? saveChanges() : makeEditable()"
        :icon="editState ? 'mdi-content-save' : 'mdi-pencil'"
      ></v-icon-btn>
      <v-col cols="5">
        Pipeline Name:<v-text-field
          solo
          :disabled="!editState"
          v-model="pipelineName"
        ></v-text-field>
      </v-col>
      <v-col cols="5">
        AE title:<v-text-field
          solo
          :disabled="!editState"
          v-model="pipelineAETitle"
        ></v-text-field>
      </v-col>
      <v-col cols="2">
        <v-checkbox 
          v-model="pipelineIsShared"
          label="Shared"
          :false-value="false"
          :true-value="true"
          :disabled="!editState"
        />
      </v-col>
      <v-col cols="6">
        Results from this Pipeline
        <PipelineResults :pipelineId="this.pipelineId" />
      </v-col>
      <v-col cols="6">
        More Info
        <PipelineTreeviewInfo :pipelineId="this.pipelineId" />
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { generic_get, generic_put } from '~/api'
import vIconBtn from './global/v-icon-btn.vue'
import PipelineTreeviewInfo from './PipelineTreeviewInfo'
import PipelineResults from '~/components/pipeline/PipelineResults'
export default {
  components: { vIconBtn, PipelineResults, PipelineTreeviewInfo },
  props: {
    pipelineId: {
      type: String
    }
  },
  data() {
    return {
      pipelineName: '',
      pipelineAETitle: '',
      pipelineIsShared: '',
      editState: false
    }
  },
  methods: {
    async saveChanges() {
      try {
        const URL = `/pipeline/${this.pipelineId}/edit`
        const payload = {
          name: this.pipelineName,
          ae_title: this.pipelineAETitle,
          is_shared: this.pipelineIsShared
        }
        console.log(payload)
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
    },
    async getPipelineName() {
      // get Pipeline Name and AE Title
      const URL = `/pipeline/${this.pipelineId}`
      const {name, ae_title, is_shared} = await generic_get(this, URL)
      this.pipelineName = name
      this.pipelineAETitle = ae_title
      this.pipelineIsShared = is_shared
      console.log(is_shared)
      console.log(this.pipelineIsShared)
    }
  },
  created() {
    this.getPipelineInfo()
  }
}
</script>
