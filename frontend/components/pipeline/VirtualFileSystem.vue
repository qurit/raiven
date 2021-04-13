<template>
  <div>
    <v-card elevation="6" class="mt-4">
      <v-toolbar :color="toolbarColor" flat>
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
        <v-icon-btn
          v-if="!deleteMode"
          @click="getPipelineRunFiles"
          :color="toolbarIconColor"
          refresh
        />
        <v-icon-btn
          v-if="!deleteMode"
          @click="deleteMode = true"
          :color="toolbarIconColor"
          delete
        />
        <v-icon-btn
          v-if="deleteMode"
          @click="clearDelete"
          :color="toolbarIconColor"
          close
        />
        <v-icon-btn
          v-if="deleteMode"
          @click="saveDelete"
          :color="toolbarIconColor"
          deleteEmpty
        />
      </v-toolbar>
      <v-data-table
        id="VFS"
        v-model="selected"
        :show-select="deleteMode"
        :items="items"
        :headers="headers"
        :search="search"
        :sort-by.sync="sortBy"
        :items-per-page="10"
      >
        <template v-slot:[`item.actions`]="{ item }">
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
import vIconBtn from '../global/v-icon-btn.vue'

export default {
  name: 'VirtualFileSystem',
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
    search: '',
    selected: [],
    deleteMode: false
  }),
  computed: {
    toolbarColor: ctx => (ctx.deleteMode ? 'error' : 'primary accent--text'),
    toolbarIconColor: ctx => (ctx.deleteMode ? 'white' : 'accent')
  },
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
      var fileURL = window.URL.createObjectURL(new Blob([resultFile]))
      var fileLink = document.createElement('a')
      fileLink.href = fileURL
      fileLink.setAttribute('download', `${file.filename}`)
      document.body.appendChild(fileLink)
      fileLink.click()
    },
    clearDelete() {
      this.deleteMode = false
      this.selected = []
    },
    async saveDelete() {
      if (
        window.confirm('Are you sure you want to delete the selected items?')
      ) {
        this.deleteMode = false
        for (const file of this.selected) {
          try {
            await generic_delete(this, `/vfs/${file.id}`)
          } catch (e) {
            this.$toaster.toastError('Could not delete run: ' + file.id)
          }
        }
        this.selected = []
        await this.getPipelineRunFiles()
      }
    }
  }
}
</script>
