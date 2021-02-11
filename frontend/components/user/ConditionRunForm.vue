<template>
  <v-card class="overflow-x-hidden">
    <v-card-title>Add a Condition</v-card-title>
    <v-card-subtitle>Start a pipeline when only a specific series has been received</v-card-subtitle>
    <v-card-text>
      <v-row>
        <v-col>
          <v-select
            v-model="pipelineId"
            :items="pipelines"
            item-text="name"
            item-value="id"
            label="Choose a pipeline"
            class="mx-2"
            solo
            flat
          />
        </v-col>
      </v-row>
    </v-card-text>

    <v-row justify="center" align="center">
      <v-btn
        text
        class="ma-4"
        color="confirm"
        @click="submit"
        :disabled="
          !conditionName || currentConditions.length === 0 || !pipelineId
        "
      >
        Save
      </v-btn>
    </v-row>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import {toPropFormat} from "@/utilities/propHelpers";

export default {
  data() {
    return {
      pipelineId: '',
      isActive: false,
      conditionName: '',
      textFieldAttrs: toPropFormat(['solo', 'single-line', 'hide-details', 'dense', 'flat']),
      types: ['Node', 'Patient', 'Study', 'Series'],
      newConditionIdentifier: '',
      newConditionType: '',
      currentConditions: []
    }
  },
  methods: {
    addCondition() {
      const type = this.newConditionType
      const identifier = this.newConditionIdentifier
      this.currentConditions.push({ type, identifier })
      this.newConditionType = null
      this.newConditionIdentifier = null
    },
    removeCondition(index) {
      this.currentConditions.splice(index, 1)
    },
    submit() {
      const payload = {}
      payload['pipeline'] = this.pipelineId
      payload['isActive'] = this.isActive
      payload['conditionName'] = this.conditionName
      payload['conditions'] = {}
      this.currentConditions.forEach(condition => {
        payload.conditions[condition.type]
          ? payload.conditions[condition.type].push(condition.identifier)
          : (payload.conditions[condition.type] = [condition.identifier])
      })
      this.$store.dispatch('conditions/addCondition', payload)
      this.$emit('closeDialog')
      this.currentConditions = []
      this.newConditionIdentifier = null
      this.newConditionType = null
      this.isActive = false
      this.conditionName = null
      this.pipelineId = null
    }
  },
  created() {
    this.$store.dispatch('pipelines/fetchPipelines')
  },
  computed: {
    ...mapState('pipelines', ['pipelines'])
  }
}
</script>
