<template>
  <v-card class="mx-auto" elevation="6">
    <v-card-title>
      Received DICOM Instances
    </v-card-title>
    <v-divider light />

    <!-- Nodes   -->
    <v-treeview
      dense
      :items="nodes"
      item-text="id"
      activatable
      :loadChildren="fetchTest"
    >
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
      // if opening the node accordion
      if (item.hasOwnProperty('host')) {
        return (
          axios
            .get(`http://localhost:5000/dicom/nodes/${item.id}/patients`)
            // appending "children" to the patients so that they are openable
            .then(res => {
              res.data.forEach(patient => {
                patient['children'] = []
              })
              return res.data
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
      // if opening the patient accordion
      if (item.hasOwnProperty('patient_id')) {
        return (
          axios
            .get(
              `http://localhost:5000/dicom/nodes/${item.dicom_node_id}/patient/${item.id}/studies`
            )
            // append "children" to the studies so that they are openable
            .then(res => {
              res.data.forEach(study => {
                study['children'] = []
              })
              return res.data
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
      if (item.hasOwnProperty('study_date')) {
        return axios
          .get(
            `http://localhost:5000/dicom/patient/${item.dicom_patient_id}/study/${item.id}/series`
          )
          .then(res => {
            res.data.forEach(studies => {
              // adding the studies to the series' children
              item.children.push(studies)
            })
          })
          .catch(err => console.log(err))
      }
    },
    async getNodes() {
      const blah = await axios
        .get('http://localhost:5000/dicom/nodes')
        .then(res => {
          this.nodes = res.data
        })
      // appending "children" to each node so its openable
      this.nodes.forEach(node => {
        this.$set(node, 'children', [])
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
