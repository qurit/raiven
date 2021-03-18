<template>
  <div>
    <v-card elevation="6">
      <v-toolbar :color="toolbarColor" flat v-if="!this.pipelineId">
        <v-toolbar-title>
          <b>Pipeline Run Results </b>
        </v-toolbar-title>
        <v-spacer />
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search by Run ID or Pipeline"
          hide-details
          solo
        />
        <v-icon-btn v-if="!deleteMode" @click="getPipelineRuns" :color="toolbarIconColor" refresh />
        <v-icon-btn v-if="!deleteMode" @click="deleteMode = true" :color="toolbarIconColor"  delete />
        <v-icon-btn v-if="deleteMode" @click="clearDelete" :color="toolbarIconColor" close />
        <v-icon-btn  v-if="deleteMode" @click="saveDelete" :color="toolbarIconColor" save />
      </v-toolbar>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        :label="
          !!this.pipelineId
            ? 'Search by Run ID'
            : 'Search by Run ID or Pipeline'
        "
        hide-details
        v-if="!!this.pipelineId"
        class="mx-4"
      />

      <v-data-table
        id="ResultsTable"
        v-model="selected"
        :show-select="deleteMode"
        :headers="headers"
        :items="items"
        :search="search"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :loading="fetching"
        :items-per-page="5"
        loading-text="Getting Results..."
      >
        <template v-slot:item.created_datetime="{ item }">{{
          formatDateTime(item.created_datetime)
        }}</template>
        <template v-slot:item.finished_datetime="{ item }">{{
          formatDateTime(item.finished_datetime)
        }}</template>
        <template v-slot:item.actions="{ item }">
          <v-icon small class="mr-2" @click="download(item)">
            mdi-download
          </v-icon>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import { generic_get, generic_delete } from '~/api'
import { downloadFile } from "@/utilities/files";
import vIconBtn from '../global/v-icon-btn.vue'

export default {
  components: { vIconBtn },
  props: {
    pipelineId: {
      type: Number
    }
  },
  data: () => ({
    headers: [
      { text: 'Run ID', align: 'start', value: 'id' },
      { text: 'Status', value: 'status' },
      { text: 'Started on:', filterable: false, value: 'created_datetime' },
      { text: 'Finished on:', filterable: false, value: 'finished_datetime' },
      { text: 'Results', value: 'actions', sortable: false, align: 'center' }
    ],
    items: [],
    sortBy: 'finished_datetime',
    sortDesc: true,
    search: '',
    fetching: true,
    selected: [],
    deleteMode: false
  }),
  computed: {
    toolbarColor: ctx => ctx.deleteMode ? 'error' : 'primary accent--text',
    toolbarIconColor: ctx => ctx.deleteMode ? 'white' : 'accent'
  },
  created() {
    this.getPipelineRuns()
    if (!this.pipelineId)
      this.headers.splice(1, 0, { text: 'Pipeline', value: 'pipeline.name' })
  },
  methods: {
    formatDateTime: x => (x ? new Date(x).toLocaleString() : 'Invalid Date'),
    formatFileName: x => `${x.pipeline.name}_results_${x.finished_datetime}.zip`,
    async getPipelineRuns() {
      const URL = this.pipelineId
        ? `/pipeline/${this.pipelineId}/results`
        : '/pipeline/results'
      const pipelineRuns = await generic_get(this, URL)
      this.items = pipelineRuns
      this.fetching = false
    },
    download(pipelineRun) {
      /**
       * I am so sorry for my sins but axios does not support streaming responses so I had to write this jank thing
       */

      const URL = `${this.$axios.defaults.baseURL}/pipeline/download/${pipelineRun.id}`
      const FILENAME = this.formatFileName(pipelineRun)
      downloadFile(this, URL, FILENAME)
    },
    clearDelete() {
      this.deleteMode = false;
      this.selected = []
    },
    async saveDelete() {
      if (window.confirm("Are you sure you want to delete the selected items")) {
        this.deleteMode = false;

        for (const run of this.selected) {
          try {
            await generic_delete(this, `/pipeline/run/${run.id}`)
          } catch (e) {
            this.$toaster.toastError('Could not delete run: ' + run.id)
          }
        }

        this.selected = []
        await this.getPipelineRuns()
      }
    }
  }
}
</script>
<style>
#ResultsTable > div > table > tbody > tr > td {
  text-transform: capitalize;
}
</style>
