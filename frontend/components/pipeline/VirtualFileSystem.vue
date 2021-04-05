<template>
  <div>
    <v-card elevation="6" class="mt-4">
      <v-toolbar color="primary accent--text" flat>
        <v-toolbar-title>
          <b>Files from Pipeline Runs </b>
        </v-toolbar-title>
        <v-spacer />
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          hide-details
          solo
        />
        <v-icon-btn @click="getPipelineRunFiles" color="#373740" refresh />
      </v-toolbar>
      <v-data-table
        id="VFS"
        :items="items"
        :headers="headers"
        :search="search"
        :sort-by.sync="sortBy"
        :loading="fetching"
        :items-per-page="10"
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
import { generic_get } from '~/api'
import vIconBtn from '../global/v-icon-btn.vue'

export default {
  components: { vIconBtn },
  data: () => ({
    headers: [
      { text: 'Run ID', value: 'pipeline_run_id' },
      { text: 'Type', value: 'type' },
      { text: 'Filename', value: 'filename' },
      { text: 'Download', value: 'actions', sortable: false, align: 'center' }
    ],
    items: [],
    sortBy: 'pipeline_run_id',
    search: ''
  }),
  created() {
    this.getPipelineRunFiles()
  },
  methods: {
    async getPipelineRunFiles() {
      const URL = '/vfs'
      const virtualFileSystem = await generic_get(this, URL)
      this.items = virtualFileSystem
    },
    async download(file) {
      const URL = `/vfs/${file.id}`
      const resultFile = await generic_get(this, URL, { responseType: 'blob' })
      console.log(resultFile)
      var fileURL = window.URL.createObjectURL(new Blob([resultFile]))
      var fileLink = document.createElement('a')
      fileLink.href = fileURL
      fileLink.setAttribute('download', `${file.filename}`)
      document.body.appendChild(fileLink)
      fileLink.click()
    }
  }
}
</script>
