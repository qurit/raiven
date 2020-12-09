<template>
  <v-card class="overflow-x-hidden">
  <v-form v-model="isFormValid">
    <v-text-field
      v-model="pipelineName"
      label="Pipeline Name*"
      required
      :rules="[v => !!v || 'A Pipeline Name is required']"
      class="px-15 pt-10"
    />
    <v-text-field
      v-model="aeTitle"
      label="AE Title"
      class="px-15"
      :rules="[rules.validateLength, rules.validateASCII]"
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
        <v-btn
        @click="savePipeline"
        :disabled="!isFormValid"
        class="ma-4"
        color="confirm"
        text
      >
        Save
      </v-btn>
    </v-row>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      isFormValid: false,
      pipelineName: '',
      aeTitle: '',
      rules: {
        validateLength(value) {
          return (
            value.trim().length <= 12 ||
            'AE Title is too long, 12 characters max'
          )
        },
        validateASCII(value) {
          if (!!value) {
            return /^[\x00-\x7F]*$/.test(value) || 'ASCII Characters only'
          }
        }
      },
      isShared: false
    }
  },
  methods: {
    async savePipeline() {
      try {
          const payload = {
        name: this.pipelineName,
        ae_title: this.aeTitle.trim().length > 0 ? 'RVP-' + this.aeTitle.trim() : null,
        is_shared: this.isShared
      }
      console.log(payload)
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
