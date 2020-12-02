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
  props: [
    'dicom_obj_type',
    'dicom_obj_id',
    'nodes',
    'patients',
    'studies',
    'series'
  ],

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
        // api delete
        const URL = `/dicom/${this.dicom_obj_type.toLowerCase()}/${
          this.dicom_obj_id
        }/`
        await generic_delete(this, URL)

        // update treeview in frontend
        // had to "rebuild" the treeview somewhat and instead of looping through the whole treeview
        // thought it would be easier to split them up and search for the deleted node/patient/study/series
        // and then rebuild it from there to update
        let updatedNodes = true
        switch (this.dicom_obj_type) {
          case 'Node':
            this.nodes = this.nodes.filter(
              node => node.id !== this.dicom_obj_id
            )
            break
          case 'Patient':
            let dicomNodeId
            // find which node this patient came from
            this.patients.forEach(patient => {
              if (patient.id === this.dicom_obj_id) {
                dicomNodeId = patient.dicom_node_id
              }
            })
            // delete the patient from the patient-tree
            this.patients = this.patients.filter(
              patient => patient.id !== this.dicom_obj_id
            )
            // update that node's children to have the updated patient tree
            this.nodes.forEach(node => {
              if (node.id === dicomNodeId) {
                node.children = this.patients
              }
            })
            break
          case 'Study':
            let patientId
            this.studies.forEach(study => {
              if (study.id === this.dicom_obj_id) {
                patientId = study.dicom_patient_id
              }
            })
            this.studies = this.studies.filter(
              study => study.id !== this.dicom_obj_id
            )
            this.patients.forEach(patient => {
              let dicomNodeId
              if (patient.id === patientId) {
                patient.children = this.studies
                dicomNodeId = patient.dicom_node_id
              }
            })
            this.nodes.forEach(node => {
              if (node.id === dicomNodeId) {
                node.children = this.patients
              }
            })
            break
          case 'Series':
            let studyId
            this.series.forEach(s => {
              if (s.id === this.dicom_obj_id) {
                studyId = s.dicom_study_id
              }
            })
            this.series = this.series.filter(
              series => series.id !== this.dicom_obj_id
            )
            this.studies.forEach(study => {
              let patientId
              if (study.id === studyId) {
                study.children = this.series
                patientId = study.dicom_patient_id
              }
            })
            this.patients.forEach(patient => {
              let dicomNodeId
              if (patient.id === patientId) {
                patient.children = this.studies
                dicomNodeId = patient.dicom_node_id
              }
            })
            this.nodes.forEach(node => {
              if (node.id === dicomNodeId) {
                node.children = this.patients
              }
            })
            break
          default:
            // if something fell through, then could not get updated correctly
            updatedNodes = false
        }
        if (!!updatedNodes) {
          {
            this.$emit('test', this.nodes)
            this.$toaster.toastSuccess(
              this.dicom_obj_type +
                ' ' +
                this.dicom_obj_id.toString() +
                ' deleted!'
            )
            this.$emit('closeDialog')
          }
        } else {
          this.$toaster.toastError('Something went wrong')
        }
      } catch (e) {
        this.$toaster.toastError(e)
      }
    }
  }
}
</script>
