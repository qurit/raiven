<template>
  <v-card class="mx-auto" elevation="6">
    <v-card-title>
      Received DICOM Instances
    </v-card-title>
    <v-divider light />

    <!-- Nodes   -->
    <v-treeview dense :items="nodes" item-text="id" :loadChildren="fetchTest">
      <template slot="label" slot-scope="{ item }">
        <a v-if="item.hasOwnProperty('host')" @click="send('Node', item.id)">
          From Host: {{ item.host }}
        </a>
        <a
          v-else-if="item.hasOwnProperty('patient_id')"
          @click="send('Patient', item.id)"
        >
          {{ item.id }} Patient: {{ item.patient_id }}
        </a>
        <a
          v-else-if="item.hasOwnProperty('study_instance_uid')"
          @click="send('Study', item.id)"
        >
          Study Date: {{ item.study_date }}
        </a>
        <a v-else @click="send('Series', item.id)">
          Series: {{ item.series_instance_uid }}
        </a>
      </template></v-treeview
    >
    <v-btn @click="tester"> test </v-btn>
    <v-treeview dense :items="items"> </v-treeview>
    <v-dialog v-model="dialog" width="500px" height="600px">
      <DicomForm
        :dicom_obj_type="dicom_obj_type"
        :dicom_obj_id="dicom_obj_id"
        @submit="dialog = false"
      />
    </v-dialog>
  </v-card>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import DicomForm from './DicomForm'
import ContainerForm from '~/components/container/ContainerForm'
import { generic_get } from '~/api'
import dicomfilesVue from '../../pages/dicomfiles.vue'

export default {
  components: { ContainerForm, DicomForm },
  data: () => ({
    dialog: false,
    dicom_obj_type: undefined,
    dicom_obj_id: undefined,
    nodes: undefined
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
              })
              return data
            })
            // adding the patients as the node's children
            .then(patients => {
              patients.forEach(patient => {
                item.children.push(patient)
              })
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
              })
              return data
            })
            // adding the studies as the patient's children
            .then(studies => {
              studies.forEach(study => {
                item.children.push(study)
              })
            })
            .catch(err => console.log(err))
        )
      }
      // open study accordion / get series
      if (item.hasOwnProperty('study_date')) {
        const URL = `/dicom/patient/${item.dicom_patient_id}/study/${item.id}/series`
        return generic_get(this, URL)
          .then(data => {
            data.forEach(studies => {
              // adding the studies to the series' children
              item.children.push(studies)
            })
          })
          .catch(err => console.log(err))
      }
    },
    async getNodes() {
      const URL = '/dicom/nodes'
      await generic_get(this, URL)
        .then(data => {
          this.nodes = data
        })
        .then(() => {
          this.nodes.forEach(node => {
            this.$set(node, 'children', [])
          })
        })
    },
    send(type, id) {
      this.dicom_obj_type = type
      this.dicom_obj_id = id
      this.dialog = true
    },
    async submit() {
      this.dialog = false
    }
  }
}
</script>
