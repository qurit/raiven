<template>
  <v-card class="overflow-x-hidden">
    <v-text-field
      v-model="pipelineName"
      label="Pipeline Name*"
      required
      :rules="[v => !!v || 'A Pipeline Name is required']"
      class="px-15 pt-10"
    />
    <v-text-field v-model="aeTitle" label="AE Title" class="px-15" />
    <v-row justify="center" align="center">
      <v-btn
        @click="savePipeline"
        :disabled="this.isDisabled"
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
      pipelineName: '',
      aeTitle: ''
    }
  },
  methods: {
    async savePipeline() {
      const payload = {
        name: this.pipelineName,
        ae_title: this.aeTitle
      }
      const { data } = await this.$store.dispatch(
        'pipelines/addPipeline',
        payload
      )
      this.$toaster.toastSuccess('Pipeline created!')
      this.$router.push({ path: `/pipeline/${data.id}` })
      this.$emit('closeDialog')
    }
  }
}
</script>
