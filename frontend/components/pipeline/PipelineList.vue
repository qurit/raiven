<template>
  <v-card
    elevation="6"
    max-height="750"
    class="overflow-y-auto overflow-x-hidden"
    :class="'dark'"
  >
    <v-card-header
      title="Your Pipelines"
      v-model="search"
      searchable
      icon="plus"
      :func="openAddPipelineForm"
    />
    <v-data-table
      id="Pipelines"
      :headers="headers"
      :items="items"
      :search="search"
      class="row-pointer"
      @click:row="viewPipeline"
    >
      <template v-slot:[`item.is_shared`]="{ item }">
        <v-simple-checkbox :value="item.is_shared" disabled />
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon medium @click.stop="deletePipeline(item.id)" color="cancel">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="addPipelineDialog" max-width="600px">
      <AddPipelineForm @closeDialog="addPipelineForm = false" />
    </v-dialog>
    <v-dialog
      v-model="confirmDeleteDialog"
      max-width="525px"
      min-height="600px"
    >
      <v-card class="overflow-x-hidden">
        <v-card-title style="word-break: break-word">
          Deleting this pipeline will clear all of its run results as well.
        </v-card-title>
        <v-card-subtitle>
          Are you sure you want to continue?
        </v-card-subtitle>
        <v-card-actions class="justify-center">
          <v-btn text color="confirm" @click="confirmDeletePipeline">
            Yes
          </v-btn>
          <v-btn text color="cancel" @click="confirmDeleteDialog = false">
            No
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import { AddPipelineForm } from '~/components/pipeline'
import { mapState } from 'vuex'

export default {
  name: 'PipelineList',
  components: {
    AddPipelineForm
  },
  data: function() {
    return {
      addPipelineDialog: false,
      confirmDeleteDialog: false,
      deletePipelineId: null,
      dialog: false,
      headers: [
        { text: 'Pipeline Name', value: 'name' },
        { text: 'AE Title', value: 'ae_title' },
        { text: 'Shared', value: 'is_shared', align: 'center' },
        {
          text: 'Delete',
          value: 'actions',
          sortable: false,
          align: 'center'
        }
      ],
      search: ''
    }
  },
  computed: {
    ...mapState('pipelines', ['pipelines']),
    items() {
      return this.$store.getters['pipelines/userPipelines']
    }
  },
  created() {
    this.$store.dispatch('pipelines/fetchPipelines')
  },
  methods: {
    openAddPipelineForm() {
      this.addPipelineDialog = true
    },
    viewPipeline(pipeline) {
      this.$router.push({ path: `/pipeline/${pipeline.id}` })
    },
    async confirmDeletePipeline() {
      try {
        await this.$store.dispatch(
          'pipelines/deletePipeline',
          this.deletePipelineId
        )
        this.$toaster.toastSuccess('Pipeline deleted!')
      } catch (e) {
        this.$toaster.toastError('Could not delete pipeline!')
      }
      this.confirmDeleteDialog = false
    },
    deletePipeline(pipelineId) {
      this.deletePipelineId = pipelineId
      this.confirmDeleteDialog = true
    }
  }
}
</script>

<style lang="css" scoped>
.row-pointer >>> tbody tr :hover {
  cursor: pointer;
}
</style>
