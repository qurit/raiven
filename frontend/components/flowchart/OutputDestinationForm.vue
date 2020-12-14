<template>
  <v-card class="overflow-x-hidden">
    <v-form v-model="isFormValid" class="ma-5" ref="form">
      <v-card-title> Add a destination source for your pipelines</v-card-title>
      <v-row>
        <v-col cols="6">
          <v-text-field
            v-model="host"
            label="Host Address"
            :rules="[v => !!v || 'A Host Address is required']"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model.number="port"
            label="Port"
            :rules="[rules.validateNumber]"
            required
          ></v-text-field>
        </v-col>
      </v-row>
    </v-form>
    <v-row justify="center">
      <v-btn
        :disabled="!this.isFormValid"
        @click="submit"
        color="confirm"
        class="ma-4"
        text
      >
        Add destination
      </v-btn>
    </v-row>
  </v-card>
</template>

<script>
export default {
  name: 'OutputDestinationForm',
  data: () => ({
    isFormValid: false,
    rules: {
      validateNumber(value) {
        return Number.isInteger(value) || 'Port must be a number'
      }
    },
    host: '',
    port: ''
  }),
  methods: {
    async submit() {
      this.$store.dispatch('destination/addDestination', {
        host: this.host,
        port: this.port
      })
      this.$refs.form.reset()
      this.$emit('closeDialog')
    }
  }
}
</script>
