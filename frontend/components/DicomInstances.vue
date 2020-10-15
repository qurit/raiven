<template>
  <v-card class="mx-auto" elevation="6">
    <v-card-title>
      Received DICOM Instances
    </v-card-title>
    <v-divider light />
    <v-list-item v-for="dicomEvent in dicomEvents" :key="dicomEvent.id">
      <v-list-group :value="true" no-action :ripple="false">
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title
              >{{ dicomEvent.id }}. Host:
              {{ dicomEvent.host }}</v-list-item-title
            >
          </v-list-item-content>
        </template>
        <v-list-group no-action sub-group :ripple="false">
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Patients</v-list-item-title>
            </v-list-item-content>
          </template>
          <v-list-item
            v-for="dicomPatient in dicomEvent.dicom_patient"
            :key="dicomPatient.id"
          >
            <v-list-group no-action sub-group :ripple="false">
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title>
                    Patient
                    {{ dicomPatient.patient_id }} Studies</v-list-item-title
                  >
                </v-list-item-content>
              </template>
              <v-list-item
                v-for="dicomStudy in dicomPatient.dicom_study"
                :key="dicomStudy.id"
              >
                <v-list-group no-action sub-group :ripple="false">
                  <template v-slot:activator>
                    <v-list-item-content>
                      <v-list-item-title>
                        Study {{ dicomStudy.study_instance_uid }} Series
                      </v-list-item-title>
                    </v-list-item-content>
                  </template>
                  <v-list-item
                    v-for="dicomSeries in dicomStudy.dicom_series"
                    :key="dicomSeries.id"
                  >
                    {{ dicomSeries.series_instance_uid }}
                  </v-list-item>
                </v-list-group>
              </v-list-item>
            </v-list-group>
          </v-list-item>
        </v-list-group>
      </v-list-group>
    </v-list-item>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState('dicomEvents', ['dicomEvents'])
  },
  created() {
    this.$store.dispatch('dicomEvents/fetchDicomEvents')
  }
}
</script>
