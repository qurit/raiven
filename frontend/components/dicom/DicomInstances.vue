<template>
  <v-card class="mx-auto" elevation="6">
    <v-card-title>
      Received DICOM Instances
    </v-card-title>
    <v-divider light />

    <!-- Nodes   -->
    <v-list-item v-for="dicomEvent in dicomEvents" :key="dicomEvent.id">
      <v-list-group
        :value="true"
        no-action
        :ripple="false"
        @click="loadPatientContent(dicomEvent.id)"
      >
        <v-btn
          color="blue"
          small
          :ripple="false"
          @click="send('node', dicomEvent.id)"
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

        <!-- Patients -->
        <!-- NEED TO FIX THE THING.. SEEMS LIKE ITS BECAUSE ITS AUTO OPENED? OR SOMETHING? -->
        <div v-if="dicomNodes[dicomEvent.id] !== undefined">
          <v-list-item
            v-for="dicomPatient in dicomNodes[dicomEvent.id].patients"
            :key="dicomPatient.id"
          >
            <v-list-group
              no-action
              sub-group
              :ripple="false"
              @click="loadStudyContent(dicomEvent.id, dicomPatient.id)"
            >
              <v-btn
                color="blue"
                small
                :ripple="false"
                class="ml-16"
                @click="send('patient', dicomPatient.id)"
              >
                Send Patient {{ dicomPatient.id }} to a Pipeline
              </v-btn>
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title
                    >{{ dicomPatient.id }} Patient
                    {{ dicomPatient.patient_id }}</v-list-item-title
                  >
                </v-list-item-content>
              </template>

              <!-- Studies -->
              <div v-if="dicomNodes[dicomEvent.id].patients[dicomPatient.id]">
                <v-list-item
                  v-for="dicomStudy in dicomNodes[dicomEvent.id].patients[
                    dicomPatient.id
                  ].studies"
                  :key="dicomStudy.id"
                >
                  <v-list-group
                    no-action
                    sub-group
                    :ripple="false"
                    @click="loadSeriesContent"
                  >
                    <v-btn
                      color="blue"
                      small
                      :ripple="false"
                      class="ml-16"
                      @click="send('study', dicomStudy.id)"
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

                    <!-- Series -->
                    <!-- <v-list-item
                    v-for="dicomSeries in dicomStudy.series"
                    :key="dicomSeries.id"
                  >
                    {{ dicomSeries.series_description }}
                    <v-btn
                      color="blue"
                      small
                      :ripple="false"
                      class="ml-6"
                      @click="send('series', dicomSeries.id)"
                    >
                      Send Series {{ dicomSeries.id }} to a Pipeline
                    </v-btn>
                  </v-list-item> -->
                  </v-list-group>
                </v-list-item>
              </div>
            </v-list-group>
          </v-list-item>
        </div>
      </v-list-group>
    </v-list-item>

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
import { mapState } from 'vuex'
import DicomForm from './DicomForm'
import ContainerForm from '~/components/container/ContainerForm'
import { generic_get } from '~/api'

export default {
  components: { ContainerForm, DicomForm },
  data: () => ({
    dialog: false,
    dicom_obj_type: undefined,
    dicom_obj_id: undefined,
    dicomNodes: {}
  }),
  computed: {
    ...mapState('dicomEvents', ['dicomEvents'])
  },
  created() {
    this.$store.dispatch('dicomEvents/fetchDicomEvents')
  },
  methods: {
    async loadPatientContent(dicomNodeId) {
      const URL = `/dicom/nodes/${dicomNodeId}/patients`
      const res = await generic_get(this, URL)
      this.dicomNodes = { [dicomNodeId]: { patients: res } }
      console.log(this.dicomNodes)
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
