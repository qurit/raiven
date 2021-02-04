<template>
   <v-card dense max-width="400">
    <v-toolbar color="primary accent--text" dense flat>{{ title }}</v-toolbar>
     <v-card-text>
       <v-form v-model="isFormValid">
         <v-row>
           <v-col cols="6">
             <v-text-field
               v-bind="textFieldAttrs"
               v-model="node.host"
               label="Host"
             />
           </v-col>
           <v-col cols="6">
             <v-text-field
               v-bind="textFieldAttrs"
               v-model="node.port"
               label="Port"
               type="number"
             />
           </v-col>
           <v-col cols="12">
             <v-text-field
               v-bind="textFieldAttrs"
               v-model="node.title"
               label="AE Title"
             />
           </v-col>
         </v-row>
       </v-form>
     </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn rounded dense small text v-text="'Cancel'" @click="$emit('close')" />
      <v-btn rounded color="primary accent--text" v-text="'Save'" small @click="submit" />
    </v-card-actions>
  </v-card>
</template>

<script>
import { toPropFormat } from "@/utilities/propHelpers";

export default {
  name: "OutputDestinationForm",
  data: () => ({
    title: 'Add Dicom Node',
    isFormValid: false,
    textFieldAttrs: toPropFormat(['solo', 'single-line', 'hide-details', 'dense', 'flat']),
    node: {
      title: undefined,
      host: undefined,
      port: undefined
    }
  }),
  methods: {
    async submit() {
      await this.$store.dispatch('destination/addDestination', this.node)
      this.$emit('close')
    }
  },
  computed: {
    isDisabled: ctx => !ctx.host || !ctx.port || !ctx.ae_title
  }
}
</script>
