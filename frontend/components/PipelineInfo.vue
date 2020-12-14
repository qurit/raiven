<template>
  <v-card elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b> About this Pipeline</b></v-toolbar-title>
      <v-spacer/>
      <v-icon-btn
        :color="isFormValid ? 'accent' : 'error'"
        @click="editState ? saveChanges() : makeEditable()"
        :icon="editState ? 'mdi-content-save' : 'mdi-pencil'"
        :disabled="editState && !isFormValid"
      />
      <v-icon-btn color="accent" close @click="$emit('close')"/>
    </v-toolbar>

    <!-- Text   -->
    <v-card-text>
      <v-row>
        <v-col sm="12" md="5">
          <v-text-field
            label="Pipeline Name"
            filled
            :disabled="!editState"
            v-model="pipelineName"
          />
        </v-col>
        <v-col sm="12" md="5">
          <v-text-field
            filled
            label="AE Title"
            :prefix="$store.state.settings.PIPELINE_AE_PREFIX"
            :disabled="!editState"
            v-model="pipelineAETitle"
             :rules="[rules.validateLength, rules.validateASCII]"
          />
        </v-col>
        <v-col sm="12" md="2">
          <v-checkbox
            v-model="pipelineIsShared"
            label="Shared"
            :false-value="false"
            :true-value="true"
            :disabled="!editState"
          />
        </v-col>

        <v-col sm="12" md="6">
          <span class="title">Results from this Pipeline</span>
          <PipelineResults :pipelineId="this.pipelineId"/>
        </v-col>
        <v-col sm="12" md="6">
          <span class="title">More Info</span>
          <PipelineTreeviewInfo :pipelineId="this.pipelineId"/>
        </v-col>
      </v-row>
    </v-card-text>

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
      isFormValid: false,
      editState: false,
       rules: {
        validateLength(value) {
          return (
            value.trim().length <= 16 ||
            'AE Title is too long, 16 characters max'
          )
        },
        validateASCII(value) {
          if (!!value) {
            return /^[\x00-\x7F]*$/.test(value) || 'ASCII Characters only'
          }
        }
      },
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
