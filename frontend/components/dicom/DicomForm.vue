<template>
  <v-card class="overflow-x-hidden">
    <v-card-title v-text="`Send ${dicom_obj_type} to Pipeline`" />
    <v-card-subtitle v-text="`ID: ${dicom_obj_id}`" class="py-0" />
    <DicomBreakdown
      :dicom_obj_type="dicom_obj_type"
      :dicom_obj_id="dicom_obj_id"
    />
    <v-card-text class="pt-0">
      All of the selected {{ dicom_obj_type.toLowerCase() }}'s contents will be
      run in the selected pipeline selected below.
      <v-select
        v-model="pipeline_id"
        :items="pipelines"
        item-text="name"
        item-value="id"
        label="Choose a pipeline"
        class="pt-2"
        solo
        flat
      />
    </v-card-text>
    <v-card-actions>
      <v-btn @click="remove" color="cancel" text>
        Delete {{ dicom_obj_type }}
      </v-btn>
      <v-spacer />
      <v-btn @click="submit" :disabled="this.isDisabled" color="confirm" text>
        Send to Pipeline
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import { generic_put, generic_delete } from '~/api'
import DicomBreakdown from '~/components/graphs/DicomBreakdown'

export default {
  props: {
    dicom_obj_type: { type: String },
    dicom_obj_id: { type: Number }
  },
  components: {
    DicomBreakdown
  },
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
        const PAYLOAD = {
          dicom_obj_type: this.dicom_obj_type,
          dicom_obj_id: this.dicom_obj_id
        }
        try {
          const data = await generic_put(this, URL, PAYLOAD)
          this.$toaster.toastSuccess(data)
          this.$emit('closeDialog')
        } catch (e) {
          this.$toaster.toastError(e)
        }
      }
    },
    async remove() {
      try {
        const URL = `/dicom/${this.dicom_obj_type.toLowerCase()}/${
          this.dicom_obj_id
        }/`
        await generic_delete(this, URL)
        this.$toaster.toastSuccess(
          this.dicom_obj_type + this.dicom_obj_id.toString() + ' deleted!'
        )
        this.$emit('closeDialog')
      } catch (e) {
        this.$toaster.toastError(e)
      }
    }
  }
}
</script>
