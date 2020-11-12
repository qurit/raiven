<template>
  <div>
    <v-card elevation="6">
      <v-toolbar color="primary accent--text" flat>
        <v-toolbar-title>
          <b>Pipeline Run Results </b>
        </v-toolbar-title>
      </v-toolbar>
      <v-data-table
        id="ResultsTable"
        :headers="headers"
        :items="items"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
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
const FileDownload = require('js-file-download')

import { generic_get } from '~/api'

export default {
  data() {
    return {
      headers: [
        { text: 'Run ID', align: 'start', value: 'id' },
        { text: 'Pipeline', value: 'pipeline.name' },
        { text: 'Status', value: 'status' },
        { text: 'Started on:', value: 'created_datetime' },
        { text: 'Finished on:', value: 'finished_datetime' },
        { text: 'Results', value: 'actions', sortable: false, align: 'center' }
      ],
      items: [],
      sortBy: 'finished_datetime',
      sortDesc: true
    }
  },
  created() {
    this.getPipelineRuns()
  },
  methods: {
    formatDateTime: x => (x ? new Date(x).toLocaleString() : 'Invalid Date'),
    formatFileName: x =>
      `${x.pipeline.name}_results_${x.finished_datetime}.zip`,
    async getPipelineRuns() {
      const URL = '/pipeline/results'
      const pipelineRuns = await generic_get(this, URL)
      this.items = pipelineRuns
    },
    async download(pipelineRun) {
      const URL = `/pipeline/download/${pipelineRun.id}`
      try {
        const results = await generic_get(this, URL, {
          responseType: 'arraybuffer'
        })
        FileDownload(results, this.formatFileName(pipelineRun))
      } catch (e) {
        this.$toaster.toastError('Could not download file')
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
