<template>
  <v-card>
    <v-card-title v-text="`Send ${dicom_obj_type} to Pipeline`"/>
    <v-card-subtitle v-text="`ID: ${dicom_obj_id}`" class="pt-0"/>
    <v-card-text>
      <v-select
      v-model="pipeline_id"
      :items="pipelines"
      item-text="name"
      item-value="id"
      label="Choose a pipeline"
      class="ma-8"
    />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn @click="submit" :disabled="this.isDisabled">
        Send to Pipeline
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import {mapState} from 'vuex'
import {generic_put} from '~/api'

export default {
  props: ['dicom_obj_type', 'dicom_obj_id'],
  data: () => ({
    pipeline_id: undefined
  }),
  created() {
    this.$store.dispatch('pipelines/fetchPipelines')
  },
  computed: {
    ...mapState('pipelines', ['pipelines']),
    isDisabled: ctx => !ctx.pipeline_id
  },
  methods: {
    async submit() {
      if (this.pipeline_id && this.dicom_obj_type && this.dicom_obj_id) {
          const URL = `/pipeline/${this.pipeline_id}`
          const PAYLOAD = {'dicom_obj_type': this.dicom_obj_type, 'dicom_obj_id': this.dicom_obj_id}

          try {
            const data =  await generic_put(this, URL, PAYLOAD)
            this.$toaster.toastSuccess(data)
            this.$emit('submit')
          } catch (e) {
            this.$toaster.toastError(e)
          }
      }
    }
  }
}
</script>
