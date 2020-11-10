<template>
  <div>
    <v-card elevation="6">
      <v-data-table
        :headers="headers"
        :items="items"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
      >
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
import { saveAs } from 'file-saver'

export default {
  data() {
    return {
      headers: [
        {
          text: 'Pipeline Run ID',
          align: 'start',
          value: 'id'
        },
        { text: 'From Pipeline', value: 'pipeline_id' },
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
    async getPipelineRuns() {
      const URL = '/pipeline/runs'
      const pipelineRuns = await generic_get(this, URL)
      this.items = pipelineRuns
    },
    async download(pipelineRun) {
      const URL = `/pipeline/download/${pipelineRun.id}`
      try {
        const results = await generic_get(this, URL, {
          responseType: 'arraybuffer'
        })
        FileDownload(
          results,
          `pipeline_run_${pipelineRun.id}_${pipelineRun.finished_datetime}.zip`
        )
      } catch (e) {
        this.$toaster.toastError('Could not download file')
      }
    }
  }
}
</script>
