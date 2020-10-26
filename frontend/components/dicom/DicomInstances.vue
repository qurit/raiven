<template>
  <v-card class="mx-auto" elevation="6">
    <v-card-title>
      Received DICOM Instances
    </v-card-title>
    <v-divider light />

    <!-- Nodes   -->
    <v-treeview
      dense
      :items="test"
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
    test: undefined,
    items: [
      {
        id: 5,
        name: 'Documents :',
        children: [
          {
            id: 6,
            name: 'vuetify :',
            children: [
              {
                id: 7,
                name: 'src :',
                children: [
                  { id: 8, name: 'index : ts' },
                  { id: 9, name: 'bootstrap : ts' }
                ]
              }
            ]
          }
        ]
      }
    ]
  }),
  computed: {
    // ...mapState('dicomEvents', ['dicomEvents']),
    // testing: function() {
    //   return (this.dicomEvents[0]['children'] = [1, 2])
    // }
  },
  created() {
    this.$store.dispatch('dicomEvents/fetchDicomEvents')
    this.tester()
  },
  methods: {
    async fetchTest(item) {
      console.log(item.hasOwnProperty('host'))
      console.log(item.hasOwnProperty('patient_id'))
      console.log(item)
      if (item.hasOwnProperty('host')) {
        return axios
          .get(`http://localhost:5000/dicom/nodes/${item.id}/patients`)
          .then(res => {
            res.data.forEach(x => {
              x['children'] = []
            })
            return res.data
          })
          .then(x => {
            console.log(x)
            x.forEach(y => {
              item.children.push(y)
            })
          })
          .catch(err => console.log(err))
      }
      if (item.hasOwnProperty('patient_id')) {
        console.log(item)
        return axios
          .get(
            `http://localhost:5000/dicom/nodes/${item.dicom_node_id}/patient/${item.id}/studies`
          )
          .then(res => {
            res.data.forEach(x => {
              x['children'] = []
            })
            return res.data
          })
          .then(x => {
            console.log(x)
            x.forEach(y => {
              item.children.push(y)
            })
          })
          .catch(err => console.log(err))
      }
      if (item.hasOwnProperty('study_date')) {
        console.log(item)
        console.log(item.parent)
        return axios
          .get(
            `http://localhost:5000/dicom/patient/${item.dicom_patient_id}/study/${item.id}/series`
          )
          .then(res => {
            res.data.forEach(x => {
              item.children.push(x)
            })
          })
          .catch(err => console.log(err))
      }
    },
    click(nodeId) {
      console.log(nodeId)
    },
    hello() {
      console.log('hello')
    },
    async tester() {
      // this.tester = await this.$store
      //   .dispatch('dicomEvents/fetchDicomEvents')
      //   .then(x => {
      //     this.test = x
      //   })
      const blah = await axios
        .get('http://localhost:5000/dicom/nodes')
        .then(x => {
          this.test = x.data
        })
      console.log('blah')
      console.log(this.test)

      this.test.forEach(x => {
        this.$set(x, 'children', [])
      })
    },
    async loadPatientContent(dicomNodeId) {
      const URL = `/dicom/nodes/${dicomNodeId}/patients`
      const res = await generic_get(this, URL)
      this.dicomNodes = { [dicomNodeId]: { patients: res } }
      // console.log(this.dicomNodes)
    },
    async loadStudyContent(dicomNodeId, patientId) {
      const URL = `/dicom/nodes/${dicomNodeId}/patient/${patientId}/studies`
      const res = await generic_get(this, URL)
      this.dicomNodes[dicomNodeId].patients.forEach(patient => {
        if (patient.id === patientId) {
          patient['studies'] = res
        }
      })
      console.log(this.dicomNodes)
      // need to somehow associate the patientId to get it dynamically, but cant set it to the array
      // index because has empty spots and stuff
      // and if i do it the object key way it gets kinda weird..., overwrites the previous dicomNode with the patient data
      // console.log(this.dicomNodes[dicomNodeId].patients[patientId].studies)
      console.log(this.dicomNodes[dicomNodeId].patients)
      console.log(this.dicomNodes[dicomNodeId].patients[0].studies)
    },
    loadSeriesContent() {
      console.log('clicked study accordion')
    },
    send(type, id) {
      console.log(type)
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
