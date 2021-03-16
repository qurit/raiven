<template>
  <v-card
    elevation="6"
    width="900"
    max-height="750"
    class="overflow-y-auto overflow-x-hidden"
    :class="'dark'"
  >
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Conditional Pipeline Runs</b></v-toolbar-title>
      <v-icon color="#373740" class="ml-2">mdi-send-check</v-icon>
      <v-spacer />
      <v-icon @click="conditionRunForm = true" color="#373740">mdi-plus</v-icon>
    </v-toolbar>
    <v-data-table id="Conditions" :headers="headers" :items="items">
      <template v-slot:item.actions="{ item }">
        <v-icon medium @click.stop="deleteCondition(item.id)" color="cancel">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="conditionRunForm" max-width="900px" min-height="600px">
      <ConditionRunForm @closeDialog="conditionRunForm = false" />
    </v-dialog>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import ConditionRunForm from './ConditionRunForm'

export default {
  components: {
    ConditionRunForm
  },
  computed: {
    ...mapState('conditions', ['conditions']),
    items() {
      const formattedConditions = JSON.parse(
        JSON.stringify(this.$store.state.conditions.conditions)
      )
      formattedConditions.forEach(condition => {
        condition.conditions = JSON.stringify(condition.conditions)
      })
      return formattedConditions
    }
  },
  data() {
    return {
      conditionRunForm: false,
      headers: [
        { text: 'Name', value: 'condition_name' },
        { text: 'Conditions', value: 'conditions' },
        { text: 'Pipeline', value: 'pipeline.name' },
        { text: 'Active', value: 'is_active' },
        {
          text: 'Delete',
          value: 'actions',
          sortable: false,
          align: 'center'
        }
      ]
    }
  },
  methods: {
    deleteCondition(conditionId) {
      this.$store.dispatch('conditions/deleteCondition', conditionId)
    }
  },
  created() {
    this.$store.dispatch('conditions/fetchConditions')
  }
}
</script>
