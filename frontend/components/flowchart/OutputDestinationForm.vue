<template>
  <v-card dense max-width="400" :loading="loading">
    <v-toolbar :color="color" dense flat>
      {{ title }}
      <v-spacer />
      <v-icon-btn
        :icon="echoIcon"
        :color="isFormValid ? 'accent' : 'white'"
        @click="$refs.form.validate() && sendEcho(node)"
      />
    </v-toolbar>
    <v-card-text>
      <v-form v-model="isFormValid" ref="form" lazy-validation>
        <v-row>
          <v-col cols="6">
            <v-text-field
              v-bind="textFieldAttrs"
              v-model="node.host"
              :rules="[validateHostAddress]"
              color="red"
              label="Host"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-bind="textFieldAttrs"
              v-model="node.port"
              :rules="[validatePort]"
              label="Port"
              type="number"
            />
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-bind="textFieldAttrs"
              v-model="node.title"
              :rules="[validateNotEmpty]"
              label="AE Title"
            />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer/>
      <v-btn rounded dense small text v-text="'Cancel'" @click="$emit('close')"/>
      <v-btn rounded :color="color" v-text="'Save'" small @click="submit"/>
    </v-card-actions>
  </v-card>
</template>

<script>
import echoMixin from "@/utilities/echoMixin";
import { toPropFormat } from "@/utilities/propHelpers";
import { validateHostAddress, validatePort, validateNotEmpty } from '@/utilities/validationRules'

export default {
  name: "OutputDestinationForm",
  mixins: [echoMixin],
  data: () => ({
    title: 'Add Dicom Node as Destination',
    echoIcon: 'mdi-wifi',
    loading: false,
    isFormValid: true,
    textFieldAttrs: toPropFormat(['solo', 'single-line', 'hide-details', 'dense', 'flat']),
    node: {
      title: 'orthanc',
      host: '127.0.0.1',
      port: '4242'
    }
  }),
  methods: {
    validateHostAddress,
    validatePort,
    validateNotEmpty,

    async submit() {
      if(this.$refs.form.validate()) {
        await this.$store.dispatch('destination/addDestination', this.node)
        this.$emit('close')
      }
    },
  },
  computed: {
    color: ({isFormValid}) => isFormValid ? 'primary accent--text' : 'error'
  }
}
</script>
