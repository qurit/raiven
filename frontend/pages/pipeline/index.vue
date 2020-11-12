<template>
  <!-- hardcode with but maybe put in columns and stuff if we figure out what to populate this page with... -->
  <v-card
    elevation="6"
    width="900"
    max-height="750"
    class="overflow-y-auto overflow-x-hidden"
    :class="'dark'"
  >
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Your Pipelines</b></v-toolbar-title>
      <v-spacer />
      <v-btn icon>
        <v-icon @click="dialog = true" color="#373740" class="pr-8"
          >mdi-pen-plus</v-icon
        >
      </v-btn>
    </v-toolbar>
    <v-divider light />
    <v-card-text>
      <v-row v-for="pipeline in pipelines" :key="pipeline.id">
        <v-col cols="8">
          <b>Pipeline Name:</b>
          {{ pipeline.name }}
        </v-col>
        <v-col cols="1">
          <v-btn small color="blue" @click="viewPipeline(pipeline.id)">
            View
          </v-btn>
        </v-col>
        <v-col cols="1">
          <v-btn small color="red" @click="removePipeline(pipeline)">
            Remove
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
    <v-dialog v-model="dialog" max-width="600px">
      <v-card class="overflow-x-hidden">
        <v-text-field
          v-model="pipelineName"
          label="Pipeline Name*"
          required
          :rules="[v => !!v || 'A Pipeline Name is required']"
          class="pa-15"
        />
        <v-row justify="center" align="center">
          <v-btn
            @click="savePipeline"
            :disabled="this.isDisabled"
            class="ma-4"
            color="green"
          >
            Save
          </v-btn>
        </v-row>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  data: function() {
    return {
      dialog: false,
      pipelineName: ''
    }
  },
  methods: {
    viewPipeline(pipelineId) {
      this.$router.push({ path: `/pipeline/${pipelineId}` })
    },
    async removePipeline(pipeline) {
      await this.$store.dispatch('pipelines/deletePipeline', pipeline.id)
      this.$toaster.toastSuccess('Pipeline removed!')
    },
    async savePipeline() {
      const payload = {
        user_id: 1,
        name: this.pipelineName
      }
      const { data } = await this.$store.dispatch(
        'pipelines/addPipeline',
        payload
      )
      this.$toaster.toastSuccess('Pipeline created!')
      this.$router.push({ path: `/pipeline/${data.id}` })
      this.dialog = false
    }
  },
  computed: {
    ...mapState('pipelines', ['pipelines']),
    isDisabled: function() {
      return !this.pipelineName
    }
  },
  created() {
    this.$store.dispatch('pipelines/fetchPipelines')
  }
}
</script>
