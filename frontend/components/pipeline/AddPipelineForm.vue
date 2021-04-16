<template>
  <v-card class="overflow-x-hidden">
    <v-card-header title="Add a Pipeline" />
    <v-form v-model="isFormValid">
      <v-text-field
        v-model="pipelineName"
        label="Pipeline Name*"
        required
        :rules="[validateNotEmpty]"
        class="px-15 pt-10"
      />
      <v-text-field
        v-model="aeTitle"
        label="AE Title"
        class="px-15"
        :rules="[validateAETitle]"
        counter
        :prefix="$store.state.config.PIPELINE_AE_PREFIX"
      />
      <v-checkbox
        v-model="isShared"
        label="Shared"
        false-value="false"
        true-value="true"
        class="px-15"
      />
    </v-form>
    <v-row justify="center" align="center">
      <v-icon-btn
        save
        :disabled="!isFormValid"
        @click="savePipeline"
        color="confirm"
        class="ma-4"
      />
    </v-row>
  </v-card>
</template>

<script>
import { validateAETitle, validateNotEmpty } from '~/utilities/validationRules'

export default {
  name: 'AddPipelineForm',
  data() {
    return {
      isFormValid: false,
      pipelineName: '',
      aeTitle: '',
      isShared: false
    }
  },
  methods: {
    validateAETitle,
    validateNotEmpty,
    async savePipeline() {
      try {
        const payload = {
          name: this.pipelineName,
          ae_title: this.aeTitle.trim().length > 0 ? this.aeTitle.trim() : null,
          is_shared: this.isShared
        }
        const { data } = await this.$store.dispatch(
          'pipelines/addPipeline',
          payload
        )
        this.$toaster.toastSuccess('Pipeline created!')
        this.$router.push({ path: `/pipeline/${data.id}` })
        this.$emit('closeDialog')
      } catch (e) {
        this.$toaster.toastError('Something went wrong')
      }
    }
  }
}
</script>
