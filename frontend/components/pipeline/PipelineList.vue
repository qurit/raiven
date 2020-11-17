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
      <template v-slot:item.actions="{ item }">
        <v-icon medium @click.stop="removePipeline(item)" color="cancel">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="dialog" max-width="600px">
      <v-card class="overflow-x-hidden">
        <v-text-field
          v-model="pipelineName"
          label="Pipeline Name*"
          required
          :rules="[v => !!v || 'A Pipeline Name is required']"
          class="pa-15"
        />
        <v-row justify="center" align="center">
          <v-btn
            @click="savePipeline"
            :disabled="this.isDisabled"
            class="ma-4"
            color="confirm"
            text
          >
            Save
          </v-btn>
        </v-row>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data: function() {
    return {
      dialog: false,
      pipelineName: '',
      headers: [
        { text: 'Pipeline Name', value: 'name' },
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
    },
    async savePipeline() {
      const payload = {
        user_id: 1,
        name: this.pipelineName
      }
      const { data } = await this.$store.dispatch(
        'pipelines/addPipeline',
        payload
      )
      this.$toaster.toastSuccess('Pipeline created!')
      this.$router.push({ path: `/pipeline/${data.id}` })
      this.dialog = false
    }
  },
  computed: {
    ...mapState('pipelines', ['pipelines']),
    isDisabled: function() {
      return !this.pipelineName
    },
    items() {
      return this.$store.state.pipelines.pipelines
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
