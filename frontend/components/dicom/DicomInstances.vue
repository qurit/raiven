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
        <a @click="click(item.id)">{{ item }}</a>
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
  },
  methods: {
    async fetchTest(item) {
      console.log(item)
      return axios
        .get('http://localhost:5000/dicom/nodes')
        .then(res => res.json())
        .then(json => item.children.push(...json))
        .catch(err => console.log(err))
    },
    click(nodeId) {
      console.log(nodeId)
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
      console.log(blah)
      console.log(this.test)
      // console.log('Dicom Events')
      // console.log(this.dicomEvents)
      this.$set(this.test[0], 'item-children', [
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
      ])
      // console.log(this.dicomEvents)
      // console.log('items')
      // console.log(this.items)
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
