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
        <div v-if="!!dicomNodes[dicomEvent.id]">
          <v-list-item
            v-for="dicomPatient in Object.entries(dicomNodes[dicomEvent.id])"
            :key="dicomPatient[0]"
          >
            <v-list-group
              no-action
              sub-group
              :ripple="false"
              @click="loadStudyContent(dicomEvent.id, dicomPatient[0])"
            >
              <v-btn
                color="blue"
                small
                :ripple="false"
                class="ml-16"
                @click="send('patient', dicomPatient)"
              >
                Send Patient {{ dicomPatient[0] }} to a Pipeline
              </v-btn>
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title
                    >{{ dicomPatient[0] }} Patient
                    {{ dicomPatient[1] }}</v-list-item-title
                  >
                </v-list-item-content>
              </template>

              <!-- Studies -->
              <v-list-item v-for="dicomStudy in [1, 2]" :key="dicomStudy.id">
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
      console.log(res)
      res.forEach(patient => {
        this.dicomNodes = {
          [dicomNodeId]: {
            [patient.id]: patient.patient_id
          }
        }
      })
      console.log(this.dicomNodes)
      console.log(Object.entries(this.dicomNodes[dicomNodeId]))
    },
    async loadStudyContent(dicomNodeId, patientId) {
      console.log(dicomNodeId)
      console.log(patientId)
      const URL = `/dicom/nodes/${dicomNodeId}/patient/${patientId}/studies`
      const res = await generic_get(this, URL)

      console.log(res)

      res.forEach(study => {
        this.dicomNodes = {
          [dicomNodeId]: {
            [patientId]: {
              [study.id]: {
                dicomPatientId: study.dicom_patient_id,
                studyDate: study.study_date,
                studyInstanceUid: study.study_instance_uid
              }
            }
          }
        }
      })
      console.log(this.dicomNodes)
      // console.log(res)
      // const studies = { [patientId]: { studies: res } }
      // this.dicomNodes
      // console.log(this.dicomNodes)
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
