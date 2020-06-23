<template>
  <v-row dense>
    <v-col>Add a Modality</v-col>
    <v-col cols="12">
      <v-text-field
        v-model="modality.aet"
        :error-messages="errors('aet')"
        label="AE Title"
        solo
        dense
      />
    </v-col>
    <v-col cols="6">
      <v-text-field
        v-model="modality.address"
        :error-messages="errors('address')"
        label="Address"
        solo
        dense
      />
    </v-col>
    <v-col cols="6">
      <v-text-field
        v-model="modality.port"
        :error-messages="errors('port')"
        label="Port"
        solo
        dense
      />
    </v-col>
  </v-row>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, integer, ipAddress } from 'vuelidate/lib/validators'

export default {
  name: "ModalityForm",
  mixins: [validationMixin],
  validations: {
    modality: {
      aet: {required},
      address: {required, ipAddress},
      port: {required, integer}
    }
  },
  data: () => ({
    title: 'Add Modality',
    modality: {
      aet: undefined,
      address: '127.0.0.0',
      port: '104'
    }
  }),
  mounted() {
    this.$root.$on('save-modality', this.save)
  },
  methods: {
    save() {
      this.$v.$touch()
      if (!this.$v.$invalid) {
        console.log('profit')
        this.$store.dispatch('modalities/addModality', this.modality)
      }
    },
    errors(field) {
      return this.$validator.getErrors(field, this.$v.modality)
    }
  }
}
</script>
