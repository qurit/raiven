<template>
  <v-card class="mx-auto" elevation="6">
    <v-card-title>
      Received DICOM Instances
    </v-card-title>
    <v-divider light />

<!-- Nodes   -->
    <v-list-item v-for="dicomEvent in dicomEvents" :key="dicomEvent.id">
      <v-list-group :value="true" no-action :ripple="false">
        <v-btn color="blue" small :ripple="false" @click="send('node', dicomEvent.id)">
          Send DICOM Node {{ dicomEvent.id }} to a Pipeline
        </v-btn>
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title>{{ dicomEvent.id }}. Received from Host: {{ dicomEvent.host }}</v-list-item-title>
          </v-list-item-content>
        </template>

<!-- Patients -->
        <v-list-item v-for="dicomPatient in dicomEvent.patients" :key="dicomPatient.id">
          <v-list-group no-action sub-group :ripple="false">
            <v-btn color="blue" small :ripple="false" class="ml-16" @click="send('patient', dicomPatient.id)">
              Send Patient {{ dicomPatient.id }} to a Pipeline
            </v-btn>
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>{{ dicomPatient.id }}. Patient {{ dicomPatient.patient_id }}</v-list-item-title>
              </v-list-item-content>
            </template>

<!-- Studies -->
            <v-list-item v-for="dicomStudy in dicomPatient.studies" :key="dicomStudy.id">
              <v-list-group no-action sub-group :ripple="false">
                <v-btn color="blue" small :ripple="false" class="ml-16" @click="send('study', dicomStudy.id)">
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
                <v-list-item v-for="dicomSeries in dicomStudy.series" :key="dicomSeries.id">
                  {{ dicomSeries.series_description }}
                  <v-btn color="blue" small :ripple="false" class="ml-6" @click="send('series', dicomSeries.id)">
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
      <DicomForm :dicom_obj_type="dicom_obj_type" :dicom_obj_id="dicom_obj_id" @submit="dialog = false" />
    </v-dialog>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import DicomForm from '../components/DicomForm'
import ContainerForm from '../components/ContainerForm'

export default {
  components: {ContainerForm, DicomForm},
  data: () => ({
      dialog: false,
      dicom_obj_type: undefined,
      dicom_obj_id: undefined,
  }),
  computed: {
    ...mapState('dicomEvents', ['dicomEvents'])
  },
  created() {
    this.$store.dispatch('dicomEvents/fetchDicomEvents')
  },
  methods: {
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
