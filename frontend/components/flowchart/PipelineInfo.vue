<template>
  <v-card elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title class="font-weight-bold"
        >About this Pipeline</v-toolbar-title
      >
      <v-spacer />
      <v-icon-btn
        @click="editState ? submit() : (editState = true)"
        :icon="editState ? 'mdi-content-save' : 'mdi-pencil'"
        color="accent"
      />
      <v-icon-btn color="accent" close @click="$emit('close')" />
    </v-toolbar>

    <!-- Text   -->
    <v-expand-transition>
      <v-card-text v-if="pipeline">
        <v-form v-model="isFormValid" ref="form">
          <v-row>
            <v-col sm="12" md="5">
              <v-text-field
                v-model="pipeline.name"
                :disabled="!editState"
                label="Pipeline Name"
                :rules="[validateNotEmpty]"
                filled
              />
            </v-col>
            <v-col sm="12" md="5">
              <v-text-field
                v-model="pipeline.ae_title"
                :prefix="$store.state.config.PIPELINE_AE_PREFIX"
                :disabled="!editState"
                :rules="[validateAETitle]"
                label="AE Title"
                filled
              />
            </v-col>
            <v-col sm="12" md="2">
              <v-checkbox
                v-model="pipeline.is_shared"
                label="Shared"
                :false-value="false"
                :true-value="true"
                :disabled="!editState"
              />
            </v-col>
            <v-col sm="12" md="6">
              <span class="title white--text">Results from this Pipeline</span>
              <PipelineResults :pipelineId="this.pipelineId" />
            </v-col>
            <v-col sm="12" md="6">
              <span class="title white--text">More Info</span>
              <PipelineTreeviewInfo :pipelineId="this.pipelineId" />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-expand-transition>
  </v-card>
</template>

<script>
import { generic_get, generic_put } from '~/api'
import PipelineTreeviewInfo from './PipelineTreeviewInfo'
import PipelineResults from '~/components/pipeline/PipelineResults'
import { validateAETitle, validateEmpty } from '~/utilities/aeTitleValidator'

export default {
  components: { PipelineResults, PipelineTreeviewInfo },
  props: {
    pipelineId: Number
  },
  data: () => ({
    pipeline: undefined,
    isFormValid: false,
    editState: false
  }),
  methods: {
    validateAETitle,
    validateEmpty,
    async submit() {
      if (!this.$refs.form.validate()) {
        this.$toaster.toastError('Invalid Form!')
      } else {
        try {
          const URL = `/pipeline/${this.pipelineId}/edit`
          await generic_put(this, URL, this.pipeline)
          this.editState = false

          this.$toaster.toastSuccess('Changes saved!')
        } catch (e) {
          this.$toaster.toastError('Could not save changes')
        }
      }
    }
  },
  async created() {
    const URL = `/pipeline/${this.pipelineId}`
    this.pipeline = await generic_get(this, URL)
  }
}
</script>
