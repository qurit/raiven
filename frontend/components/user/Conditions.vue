<template>
  <v-card
    elevation="6"
    width="900"
    max-height="750"
    class="overflow-y-auto overflow-x-hidden"
    :class="'dark'"
  >
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Scheduled Runs</b></v-toolbar-title>
      <v-icon color="#373740" class="ml-2">mdi-calendar-clock</v-icon>
      <v-spacer />
      <v-icon @click="conditionRunForm = true" color="#373740">mdi-plus</v-icon>
    </v-toolbar>
    <v-dialog v-model="conditionRunForm" max-width="900px" min-height="600px">
      <ConditionRunForm @closeDialog="conditionRunForm = false" />
    </v-dialog>
  </v-card>
</template>

<script>
import ConditionRunForm from './ConditionRunForm'

export default {
  components: {
    ConditionRunForm
  },
  data() {
    return {
      conditionRunForm: false
    }
  }
}
</script>
