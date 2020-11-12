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
    <v-text-field
      v-model="search"
      append-icon="mdi-magnify"
      label="Search"
      single-line
      hide-details
      class="px-4"
    ></v-text-field>
    <v-data-table
      id="Pipelines"
      :headers="headers"
      :items="items"
      :search="search"
    >
      <template v-slot:item.actions="{ item }">
        <v-icon
          medium
          class="mr-2"
          @click="viewPipeline(item.id)"
          color="white"
        >
          mdi-eye-outline
        </v-icon>
        <v-icon medium @click="removePipeline(item.id)" color="red">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
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
      pipelineName: '',
      headers: [
        { text: 'Pipeline Name', value: 'name' },
        {
          text: 'View or Delete',
          value: 'actions',
          sortable: false,
          align: 'center'
        }
      ],
      search: ''
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
    },
    items() {
      return this.$store.state.pipelines.pipelines
    }
  },
  created() {
    this.$store.dispatch('pipelines/fetchPipelines')
  }
}
</script>
