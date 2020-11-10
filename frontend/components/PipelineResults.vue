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
import { saveAs } from 'file-saver'
const axios = require('axios')
var JSZip = require('jszip')
const fs = require('fs')
var FileDownload = require('js-file-download')

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
    str2bytes(str) {
      var bytes = new Uint8Array(str.length)
      for (var i = 0; i < str.length; i++) {
        bytes[i] = str.charCodeAt(i)
      }
      return bytes
    },
    async test(pipelineRun) {
      const testing = await axios.get(`/pipeline/download/${pipelineRun.id}`, {
        responseType: 'blob'
      })

      var blob = new Blob([this.str2bytes(testing.data)], {
        type: 'application/zip'
      })

      saveAs(
        blob,
        `pipeline_run_${pipelineRun.id}_${pipelineRun.finished_datetime}.zip`
      )

      // .then(res => console.log(res))
      // .then(response => {
      //   FileDownload(
      //     response.data,
      //     `pipeline_run_${pipelineRun.id}_${pipelineRun.finished_datetime}.zip`
      //   )
      // })
      // const URL = `/pipeline/download/${pipelineRun.id}`
      // const blah = generic_get(this, URL)
      //   .generateAsync({ type: 'blob' })
      //   .then(function(blob) {
      //     saveAs(
      //       blob,
      //       `pipeline_run_${pipelineRun.id}_${pipelineRun.finished_datetime}.zip`
      //     )
      //   })
      // console.log(blah)

      // try {
      //   // const outputPath = pipelineRun.output_path

      //   // fs.readdir(__dirname, (err, files) => {
      //   //   if (err) console.log(err)
      //   //   else {
      //   //     console.log('\nCurrent directory filenames:')
      //   //     files.forEach(file => {
      //   //       console.log(file)
      //   //     })
      //   //   }
      //   // })
      //   // var zip = new JSZip()
      //   // zip.file('Hello.txt', 'Hello World\n')
      //   // zip.file('Goodbye.txt', 'Goodbye, cruel world\n')
      //   // zip.generateAsync({ type: 'blob' }).then(function(blob) {
      //   //   saveAs(
      //   //     blob,
      //   //     `pipeline_run_${pipelineRun.id}_${pipelineRun.finished_datetime}.zip`
      //   //   )
      //   // })
      // } catch (e) {
      //   console.log(e)
      // }
    }
  }
}
</script>
