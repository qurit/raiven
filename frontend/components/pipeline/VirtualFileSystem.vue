<template>
  <div>
    <v-card elevation="6">
      <v-toolbar color="primary accent--text" flat>
        <v-toolbar-title>
          <b>Files Created from Pipelines </b>
        </v-toolbar-title>
        <v-spacer />
        <!-- <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search by Run ID or Pipeline"
          hide-details
          solo
        /> -->
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
        class="mx-4"
      />

      <v-data-table
        id="VFS"
        :items="items"
        :headers="headers"
        :search="search"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
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
import { downloadFile } from '@/utilities/files'
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
      { text: 'Run ID', align: 'start', value: 'pipeline_run_id' },
      { text: 'Type', value: 'type' },
      { text: 'Filename', value: 'filename' },
      { text: 'Download', value: 'actions', sortable: false, align: 'center' }
    ],
    items: [],
    sortBy: 'pipeline_run_id',
    sortDesc: true,
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
    download(file) {
      console.log(file)
      /**
       * I am so sorry for my sins but axios does not support streaming responses so I had to write this jank thing
       */
      const URL = `${this.$axios.defaults.baseURL}/vfs/${file.id}`
      downloadFile(this, URL, file.type)
    },
    clearDelete() {
      this.deleteMode = false
      this.selected = []
    }
  }
}
</script>
<style>
#ResultsTable > div > table > tbody > tr > td {
  text-transform: capitalize;
}
</style>
