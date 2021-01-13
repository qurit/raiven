<template>
  <v-card class="mx-auto" elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>DICOM Instances</b></v-toolbar-title>
      <v-spacer />
      <v-icon-btn @click="getNodes" color="#373740" refresh />
    </v-toolbar>
    <DicomBreakdown />
    <p>Global:</p>
    <v-treeview
      dense
      :items="global_nodes"
      item-text="id"
      :loadChildren="fetchTest"
      hoverable
    >
      <template v-slot:prepend="{ item }">
        <v-icon v-if="item.icon" v-text="item.icon"></v-icon>
      </template>

      <template slot="label" slot-scope="{ item }">
        <a v-if="item.hasOwnProperty('host')" @click="send('Node', item.id)">
          {{ item.title }}
          <span class="text-caption"
            >Host: {{ item.host }} Port: {{ item.port }}</span
          >
        </a>
        <a
          v-else-if="item.hasOwnProperty('patient_id')"
          @click="send('Patient', item.id)"
        >
          {{ item.patient_id }}
        </a>
        <a
          v-else-if="item.hasOwnProperty('study_instance_uid')"
          @click="send('Study', item.id)"
        >
          {{ new Date(item.study_date).toLocaleDateString() }}
        </a>
        <a v-else @click="send('Series', item.id)">
          {{ item.series_description }}
        </a>
      </template>
    </v-treeview>
    <p>Private:</p>
    <DicomInstanceTree
      :nodes="private_nodes"
      :load-children="fetchTest"
      :send="send"
    />
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
import { DicomForm, DicomInstanceTree } from '~/components/dicom'
import { ContainerForm } from '~/components/container'
import { DicomBreakdown } from '~/components/graphs'
import { generic_get } from '~/api'

export default {
  components: {
    ContainerForm,
    DicomBreakdown,
    DicomForm,
    DicomInstanceTree,
  },
  data: () => ({
    dialog: false,
    dicom_obj_type: undefined,
    dicom_obj_id: undefined,
    nodes: undefined,
    global_nodes: undefined,
    private_nodes: undefined,
    patients: [],
    studies: [],
    series: [],
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
            .then((data) => {
              data.forEach((patient) => {
                patient['children'] = []
                patient.icon = 'mdi-account'
              })
              return data
            })
            // adding the patients as the node's children
            .then((patients) => {
              item.children = patients
              this.patients = patients
            })
            .catch((err) => console.log(err))
        )
      }
      // open patient accordion / get studies
      if (item.hasOwnProperty('patient_id')) {
        const URL = `/dicom/nodes/${item.dicom_node_id}/patient/${item.id}/studies`
        return (
          generic_get(this, URL)
            // append "children" to the studies so that they are openable
            .then((data) => {
              data.forEach((study) => {
                study['children'] = []
                study.icon = 'mdi-clipboard-list'
              })
              return data
            })
            // adding the studies as the patient's children
            .then((studies) => {
              item.children = studies
              this.studies = studies
            })
            .catch((err) => console.log(err))
        )
      }
      // open study accordion / get series
      if (item.hasOwnProperty('study_date')) {
        const URL = `/dicom/patient/${item.dicom_patient_id}/study/${item.id}/series`
        return generic_get(this, URL)
          .then((data) => {
            item.children = data
            this.series = data
          })
          .catch((err) => console.log(err))
      }
    },
    async getNodes() {
      const URL = '/dicom/nodes'
      await generic_get(this, URL)
        .then((data) => {
          this.nodes = data
          this.global_nodes = data.filter((node) => !node.user_id)
          console.log(data)
          this.private_nodes = data.filter(
            (node) => node.user_id == this.$auth.user.id
          )
          console.log(data)
          console.log(data[0].user_id == this.$auth.user.id)
        })
        .then(() => {
          this.nodes.forEach((node) => {
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
    updateTreeview(nodes) {
      this.nodes = nodes
    },
  },
}
</script>
