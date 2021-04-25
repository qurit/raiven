<template>
  <v-card elevation="6" flat>
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
    />
  </v-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data: () => ({
    search: '',
    selected: [],
    deleteMode: false,
    headers: [
      { text: 'Job', value: 'id' },
      { text: 'Pipeline', value: 'job.run.pipeline.name' },
      { text: 'Container Name', value: 'job.node.container.name' }
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
    clearDelete() {
      this.deleteMode = false
      this.selected = []
    }
  }
}
</script>
