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
    <v-checkbox
      v-model="isShared"
      label="Shared"
      false-value="false"
      true-value="true"
      class="px-15"
    />
    <v-row justify="center" align="center">
      <v-btn @click="savePipeline" class="ma-4" color="confirm" text>
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
      aeTitle: '',
      isShared: false
    }
  },
  methods: {
    async savePipeline() {
      const payload = {
        name: this.pipelineName,
        ae_title: this.aeTitle,
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
    }
  }
}
</script>
