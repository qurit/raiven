<template>
  <v-card class="overflow-x-hidden">
    <v-row>
      <v-col cols="12">
        <v-text-field
          label="Condition Name"
          v-model="conditionName"
          :rules="[v => !!v || 'A name is required']"
          required
          class="ma-2"
        >
        </v-text-field>
        <v-row>
          <v-card-title class="ml-2">
            Automatically send to Pipeline:
          </v-card-title>
          <v-spacer />
          <v-checkbox
            v-model="isActive"
            label="Active"
            false-value="false"
            true-value="true"
            class="pr-8"
          />
        </v-row>
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
        <v-card-title>
          When these DICOM series have been received:
        </v-card-title>
        <v-row align="center" class="mx-2">
          <v-col cols="5">
            <v-select label="Type" :items="types" v-model="newConditionType" />
          </v-col>
          <v-col cols="6">
            <v-text-field label="Idenfier" v-model="newConditionIdentifier" />
          </v-col>
          <v-col cols="1">
            <v-icon
              @click="addCondition"
              color="primary"
              :disabled="!newConditionType || !newConditionIdentifier"
              >mdi-plus</v-icon
            >
          </v-col>
        </v-row>
        <v-row
          v-for="(currentCondition, index) in currentConditions"
          class="mx-2"
          align="center"
        >
          <v-col cols="5">
            <v-text-field
              disabled
              label="Type"
              v-model="currentCondition.type"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              disabled
              label="Identifier"
              v-model="currentCondition.identifier"
            />
          </v-col>
          <v-col cols="1">
            <v-icon @click="removeCondition(index)" color="cancel"
              >mdi-delete</v-icon
            >
          </v-col>
        </v-row>
      </v-col>
    </v-row>
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

export default {
  data() {
    return {
      pipelineId: '',
      isActive: false,
      conditionName: '',
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
