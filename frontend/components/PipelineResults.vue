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
          <v-icon small class="mr-2" @click="test(item)">
            mdi-download
          </v-icon>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import { generic_get } from '~/api'
var JSZip = require('jszip')
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
    test(pipelineRun) {
      try {
        const outputPath = pipelineRun.output_path
        var zip = new JSZip()
        zip.file('Hello.txt', 'Hello World\n')
        zip.file('Goodbye.txt', 'Goodbye, cruel world\n')
        zip.generateAsync({ type: 'blob' }).then(function(blob) {
          saveAs(
            blob,
            `pipeline_run_${pipelineRun.id}_${pipelineRun.finished_datetime}.zip`
          )
        })
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>
