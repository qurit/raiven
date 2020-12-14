<template>
  <v-card elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title class="font-weight-bold">About this Pipeline</v-toolbar-title>
      <v-spacer/>
      <v-icon-btn
        @click="editState ? saveChanges() : makeEditable()"
        :icon="editState ? 'mdi-content-save' : 'mdi-pencil'"
        color="accent"
      />
      <v-icon-btn color="accent" close @click="$emit('close')"/>
    </v-toolbar>

    <!-- Text   -->
    <v-card-text>
      <v-form v-model="isFormValid" ref="form">
        <v-row>
          <v-col sm="12" md="5">
            <v-text-field
              v-model="pipelineName"
              :disabled="!editState"
              label="Pipeline Name"
              :rules="[rules.validateEmpty]"
              filled
            />
          </v-col>
          <v-col sm="12" md="5">
            <v-text-field
              v-model="pipelineAETitle"
              :prefix="$store.state.config.PIPELINE_AE_PREFIX"
              :disabled="!editState"
              :rules="[rules.validateEmpty, rules.validateLength, rules.validateASCII]"
              label="AE Title"
              filled
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
      </v-form>
    </v-card-text>

  </v-card>
</template>

<script>
import { generic_get, generic_put } from '~/api'
import PipelineTreeviewInfo from './PipelineTreeviewInfo'
import PipelineResults from '~/components/pipeline/PipelineResults'

export default {
  components: { PipelineResults, PipelineTreeviewInfo },
  props: {
    pipelineId: Number,
  },
  data() {
    return {
      pipelineName: '',
      pipelineAETitle: '',
      pipelineIsShared: '',
      isFormValid: false,
      editState: false,
       rules: {
        validateLength: v => v.trim().length <= 16 || 'AE Title is too long, 16 characters max',
        validateASCII: v => /^[\x00-\x7F]*$/.test(v) || 'ASCII Characters only',
        validateEmpty: v => !!v || 'Field Cannot be Empty'
      },
    }
  },
  methods: {
    async saveChanges() {
      if (!this.$refs.form.validate()) {
        this.$toaster.toastError('Invalid Form!')
        return
      }

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
