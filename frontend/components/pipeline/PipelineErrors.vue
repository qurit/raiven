<template>
  <v-card elevation="6" class="mt-4" flat>
    <v-toolbar :color="toolbarColor" flat>
      <v-toolbar-title>
        <b>Pipeline Errors </b>
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
      id="ErrorsTable"
      v-model="selected"
      :show-select="deleteMode"
      :headers="headers"
      :items="errors"
      :search="search"
      :items-per-page="5"
      loading-text="Getting Errors..."
    >
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon small class="mr-2" @click="openErrorMessage(item)">
          mdi-alert-circle-outline
        </v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="errorDialog" max-width="1000px" min-height="700px">
      <ErrorInfo :error="this.error" />
    </v-dialog>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import { ErrorInfo } from '~/components/flowchart'

export default {
  name: 'PipelineErrors',
  components: { ErrorInfo },
  data: () => ({
    errorDialog: false,
    error: '',
    search: '',
    selected: [],
    deleteMode: false,
    headers: [
      { text: 'Job', value: 'id' },
      { text: 'Pipeline', value: 'job.run.pipeline.name' },
      { text: 'Container Name', value: 'job.node.container.name' },
      { text: 'View', value: 'actions', sortable: false, align: 'center' }
    ]
  }),
  computed: {
    ...mapState('pipelines', ['pipelineErrors']),
    toolbarColor: ctx => (ctx.deleteMode ? 'error' : 'primary accent--text'),
    toolbarIconColor: ctx => (ctx.deleteMode ? 'white' : 'accent'),
    errors() {
      return this.$store.getters['pipelines/userPipelineErrors']
    }
  },
  created() {
    this.$store.dispatch('pipelines/fetchPipelineErrors')
  },
  methods: {
    openErrorMessage(error) {
      this.errorDialog = true
      this.error = error
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
        for (const error of this.selected) {
          try {
            await this.$store.dispatch(
              'pipelines/deletePipelineError',
              error.id
            )
            this.$toaster.toastSuccess('Error logs deleted')
          } catch (e) {
            this.$toaster.toastError('Could not delete: ' + error.id)
          }
        }
        this.selected = []
      }
    }
  }
}
</script>
