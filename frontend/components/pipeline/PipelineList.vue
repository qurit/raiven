<template>
  <v-card
    elevation="6"
    width="900"
    max-height="750"
    class="overflow-y-auto overflow-x-hidden"
    :class="'dark'"
  >
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Your Pipelines</b></v-toolbar-title>
      <v-spacer />
      <v-spacer />
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        hide-details
        solo
      />
      <v-btn icon>
        <v-icon @click="dialog = true" color="#373740">mdi-pen-plus</v-icon>
      </v-btn>
    </v-toolbar>
    <v-data-table
      id="Pipelines"
      :headers="headers"
      :items="items"
      :search="search"
      class="row-pointer"
      @click:row="viewPipeline"
    >
      <template v-slot:item.is_shared="{ item }">
        <v-simple-checkbox :value="item.is_shared" disabled />
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon medium @click.stop="removePipeline(item)" color="cancel">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="dialog" max-width="600px">
      <AddPipelineForm @closeDialog="dialog = false" />
    </v-dialog>
  </v-card>
</template>

<script>
import { AddPipelineForm } from '~/components/pipeline'
import { mapState } from 'vuex'

export default {
  components: {
    AddPipelineForm
  },
  data: function() {
    return {
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
  methods: {
    viewPipeline(pipeline) {
      this.$router.push({ path: `/pipeline/${pipeline.id}` })
    },
    async removePipeline(pipeline) {
      try {
        await this.$store.dispatch('pipelines/deletePipeline', pipeline.id)
        this.$toaster.toastSuccess('Pipeline deleted!')
      } catch (e) {
        this.$toaster.toastError('Could not delete pipeline!')
      }
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
  }
}
</script>

<style lang="css" scoped>
.row-pointer >>> tbody tr :hover {
  cursor: pointer;
}
</style>
