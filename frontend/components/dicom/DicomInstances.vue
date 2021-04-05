<template>
  <v-card class="mx-auto" elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>DICOM Instances</b></v-toolbar-title>
      <v-spacer />
      <v-icon-btn @click="getNodes" color="#373740" refresh />
    </v-toolbar>
    <DicomBreakdown />
    <div v-if="global_nodes.length">
      <p class="pl-3 pt-3 ma-0">Global:</p>
      <DicomInstanceTree
        :nodes="global_nodes"
        :load-children="fetchTest"
        @select="send"
      />
    </div>
    <div v-if="private_nodes.length">
      <p class="pl-3 pt-3 ma-0">Private:</p>
      <DicomInstanceTree
        :nodes="private_nodes"
        :load-children="fetchTest"
        @select="send"
      />
    </div>
    <v-dialog v-model="dialog" width="500px" height="600px">
      <DicomForm
        :dicom_obj_type="dicom_obj_type"
        :dicom_obj_id="dicom_obj_id"
        :nodes="nodes"
        :patients="patients"
        :studies="studies"
        :series="series"
        @closeDialog="dialog = false"
        @onDelete="updateTreeview"
      />
    </v-dialog>
  </v-card>
</template>

<script>
import { DicomForm } from '~/components/dicom'
import { DicomBreakdown } from '~/components/graphs'
import { generic_get } from '~/api'
import DicomInstanceTree from './DicomInstanceTree'

export default {
  name: 'DicomInstances',
  components: {
    DicomBreakdown,
    DicomForm,
    DicomInstanceTree
  },
  data: () => ({
    dialog: false,
    dicom_obj_type: undefined,
    dicom_obj_id: undefined,
    nodes: undefined,
    global_nodes: [],
    private_nodes: [],
    patients: [],
    studies: [],
    series: []
  }),
  created() {
    this.getNodes()
  },
  methods: {
    async fetchTest(item) {
      // open node accordion / get patients
      if (item.hasOwnProperty('host')) {
        const URL = `/dicom/nodes/${item.id}/patients`
        return (
          generic_get(this, URL)
            // append "children" to the patients so that they are openable
            .then(data => {
              data.forEach(patient => {
                patient['children'] = []
                patient.icon = 'mdi-account'
              })
              return data
            })
            // adding the patients as the node's children
            .then(patients => {
              item.children = patients
              this.patients = patients
            })
            .catch(err => console.log(err))
        )
      }
      // open patient accordion / get studies
      if (item.hasOwnProperty('patient_id')) {
        const URL = `/dicom/nodes/${item.dicom_node_id}/patient/${item.id}/studies`
        return (
          generic_get(this, URL)
            // append "children" to the studies so that they are openable
            .then(data => {
              data.forEach(study => {
                study['children'] = []
                study.icon = 'mdi-clipboard-list'
              })
              return data
            })
            // adding the studies as the patient's children
            .then(studies => {
              item.children = studies
              this.studies = studies
            })
            .catch(err => console.log(err))
        )
      }
      // open study accordion / get series
      if (item.hasOwnProperty('study_date')) {
        const URL = `/dicom/patient/${item.dicom_patient_id}/study/${item.id}/series`
        return generic_get(this, URL)
          .then(data => {
            item.children = data
            this.series = data
          })
          .catch(err => console.log(err))
      }
    },
    async getNodes() {
      const URL = `/dicom/nodes?input_node=true`
      await generic_get(this, URL)
        .then(data => this.updateTreeview(data))
        .then(() => {
          this.nodes.forEach(node => {
            this.$set(node, 'children', [])
            this.$set(node, 'icon', 'mdi-folder-network')
          })
        })
    },
    send(name, id) {
      this.dicom_obj_type = name
      this.dicom_obj_id = id
      this.dialog = true
    },
    updateTreeview(data) {
      this.nodes = data
      this.global_nodes = data.filter(node => !node.user_id)
      this.private_nodes = data.filter(
        node => node.user_id == this.$auth.user.id
      )
    }
  }
}
</script>
