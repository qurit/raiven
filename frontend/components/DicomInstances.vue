<template>
  <v-card class="mx-auto" elevation="6">
    <v-card-title>
      Received DICOM Instances
    </v-card-title>
    <v-divider light />
    <v-list-item v-for="dicomEvent in dicomEvents" :key="dicomEvent.id">
      <v-list-group :value="true" no-action :ripple="false">
        <v-btn
          color="blue"
          small
          :ripple="false"
          @click="sendNode(dicomEvent.id)"
        >
          Send DICOM Node {{ dicomEvent.id }} to a Pipeline
        </v-btn>
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title
              >{{ dicomEvent.id }}. Received from Host:
              {{ dicomEvent.host }}</v-list-item-title
            >
          </v-list-item-content>
        </template>
        <v-list-item
          v-for="dicomPatient in dicomEvent.dicom_patient"
          :key="dicomPatient.id"
        >
          <v-list-group no-action sub-group :ripple="false">
            <v-btn
              color="blue"
              small
              :ripple="false"
              class="ml-16"
              @click="sendPatient(dicomEvent.id, dicomPatient.id)"
            >
              Send Patient {{ dicomPatient.id }} to a Pipeline
            </v-btn>
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>
                  {{ dicomPatient.id }}. Patient
                  {{ dicomPatient.patient_id }}</v-list-item-title
                >
              </v-list-item-content>
            </template>
            <v-list-item
              v-for="dicomStudy in dicomPatient.dicom_study"
              :key="dicomStudy.id"
            >
              <v-list-group no-action sub-group :ripple="false">
                <v-btn
                  color="blue"
                  small
                  :ripple="false"
                  class="ml-16"
                  @click="
                    sendStudy(dicomEvent.id, dicomPatient.id, dicomStudy.id)
                  "
                >
                  Send Study {{ dicomStudy.id }} to a Pipeline
                </v-btn>
                <template v-slot:activator>
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ dicomStudy.id }}. Study date:
                      {{ dicomStudy.study_date }}
                    </v-list-item-title>
                  </v-list-item-content>
                </template>

                <v-list-item
                  v-for="dicomSeries in dicomStudy.dicom_series"
                  :key="dicomSeries.id"
                >
                  {{ dicomSeries.series_description }}
                  <v-btn
                    color="blue"
                    small
                    :ripple="false"
                    class="ml-6"
                    @click="
                      sendSeries(
                        dicomEvent.id,
                        dicomPatient.id,
                        dicomStudy.id,
                        dicomSeries.id
                      )
                    "
                  >
                    Send Series {{ dicomSeries.id }} to a Pipeline
                  </v-btn>
                </v-list-item>
              </v-list-group>
            </v-list-item>
          </v-list-group>
        </v-list-item>
      </v-list-group>
    </v-list-item>
    <v-dialog v-model="dialog" width="500px" height="600px">
      <DicomForm :nodeId="nodeId" />
    </v-dialog>
  </v-card>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import DicomForm from '../components/DicomForm'
import ContainerForm from '../components/ContainerForm'

export default {
  components: {
    ContainerForm,
    DicomForm
  },
  data: function() {
    return {
      dialog: false,
      nodeId: ''
    }
  },
  computed: {
    ...mapState('dicomEvents', ['dicomEvents'])
  },
  created() {
    this.$store.dispatch('dicomEvents/fetchDicomEvents')
  },
  methods: {
    async sendNode(nodeId) {
      this.dialog = true
      this.nodeId = nodeId
      // const res = await axios.put(`http://localhost:5000/dicom/node/${nodeId}`)
      // console.log(res.data)
    },
    async sendPatient(nodeId, patientId) {
      const res = await axios.put(
        `http://localhost:5000/dicom/node/${nodeId}/${patientId}`
      )
      console.log(res.data)
    },
    async sendStudy(nodeId, patientId, studyId) {
      const res = await axios.put(
        `http://localhost:5000/dicom/node/${nodeId}/${patientId}/${studyId}`
      )
      console.log(res.data)
    },
    async sendSeries(nodeId, patientId, studyId, seriesId) {
      const res = await axios.put(
        `http://localhost:5000/dicom/node/${nodeId}/${patientId}/${studyId}/${seriesId}`
      )
      console.log(res.data)
    }
  }
}
</script>
