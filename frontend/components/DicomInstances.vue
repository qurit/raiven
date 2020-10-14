<template>
  <v-card elevation="6">
    <v-card-title>
      DICOM events received
    </v-card-title>
    <v-list-item
      class="mx-4"
      v-for="dicomEvent in dicomEvents"
      :key="dicomEvent.id"
    >
      <!-- TODO: fix this stuff man rip -->
      Host
      {{ dicomEvent.host }}
      <br />
      Patient
      {{ dicomEvent.dicom_patient[0].patient_id }}
      <br />
      Study Instance UID
      {{ dicomEvent.dicom_patient[0].dicom_study[0].study_instance_uid }}
      <br />
      <!-- check the databse write to file -->
      Series Instance UID
      {{
        dicomEvent.dicom_patient[0].dicom_study[0].dicom_series[0]
          .series_instance_uid
      }}
      <!-- <br />
      Series
      {{ dicomEvent.dicom_patient.dicom_study.dicom_series }} -->
    </v-list-item>
    <v-btn @click="test">
      click
    </v-btn>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  methods: {
    test() {
      console.log(dicomEvents)
    }
  },
  computed: {
    ...mapState('dicomEvents', ['dicomEvents'])
  },
  created() {
    this.$store.dispatch('dicomEvents/fetchDicomEvents')
  }
}
</script>
