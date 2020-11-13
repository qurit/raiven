<template>
  <v-card class="overflow-x-hidden" width="600">
    <v-card-title> Add a destination source for your pipelines</v-card-title>
    <v-card-text>
      <v-row>

        <v-col cols="6">
          <v-text-field
            v-model="host"
            label="Host Address"
            :rules="[v => !!v || 'A Host Address is required']"
            required
          />
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="port"
            label="Port"
            :rules="[v => !!v || 'A Port is required']"
            required
          />
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="ae_title"
            label="AE Title"
            :rules="[v => !!v || 'A AE Title is required']"
            required
          />
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="nickname"
            label="Nickname"
          />
        </v-col>
      </v-row>
      </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        :disabled="this.isDisabled"
        @click="submit"
        color="confirm"
        class="ma-4"
        text
      >
        Add destination
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
  name: 'OutputDestinationForm',
  data: () => ({
    host: '',
    port: null,
    ae_title: null,
    nickname: null
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
    isDisabled: ctx => !ctx.host || !ctx.port || !ctx.ae_title
  }
}
</script>
