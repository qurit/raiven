<template>
  <v-card class="overflow-x-hidden">
    <v-form v-model="form" class="ma-5">
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
            v-model="port"
            label="Port"
            :rules="[v => !!v || 'A Port is required']"
            required
          ></v-text-field>
        </v-col>
      </v-row>
    </v-form>
    <v-row justify="center">
      <v-btn
        :disabled="this.isDisabled"
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
    host: '',
    port: null
  }),
  methods: {
    async submit() {
      this.$store.dispatch('destination/addDestination', {
        host: this.host,
        port: this.port
      })
      this.$emit('closeDialog')
    }
  },
  computed: {
    isDisabled: function() {
      return !(this.host && this.port)
    }
  }
}
</script>
