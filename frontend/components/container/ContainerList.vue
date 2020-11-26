<template>
  <v-card
    elevation="6"
    max-height="700"
    class="overflow-y-auto"
    :class="'dark'"
  >
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Your Containers</b></v-toolbar-title>
      <v-spacer />
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search by Name or File"
        hide-details
        solo
      />
    </v-toolbar>
    <v-divider light />

    <v-data-table
      id="Containers"
      :headers="headers"
      :items="items"
      :search="search"
    >
      <template v-slot:item.actions="{ item }">
        <v-icon
          medium
          class="mr-2"
          @click="editContainer(item.id)"
          color="info"
        >
          mdi-pencil
        </v-icon>
        <v-icon medium @click="deleteContainer(item.id)" color="cancel">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="dialog" max-width="900px" min-height="600px">
      <ContainerForm
        :isEditing="true"
        :containerToEdit="this.container"
        :key="this.container.containerId"
        @closeDialog="closeDialog"
      />
    </v-dialog>
    <v-dialog
      v-model="confirmDeleteDialog"
      max-width="525px"
      min-height="600px"
    >
      <v-card class="overflow-x-hidden">
        <v-card-title>
          Deleting this container will clear all pipelines with this container.
        </v-card-title>
        <v-card-subtitle>
          Are you sure you want to continue?
        </v-card-subtitle>
        <v-card-actions class="justify-center">
          <v-btn text color="confirm" @click="confirmDeleteContainer">
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
import { mapState } from 'vuex'
import ContainerForm from '~/components/container'

export default {
  components: {
    ContainerForm
  },
  data: function() {
    return {
      deleteContainerId: null,
      dialog: false,
      confirmDeleteDialog: false,
      container: {
        containerId: '',
        filename: '',
        containerName: '',
        containerDescription: '',
        containerIsInput: false,
        containerIsOutput: false
      },
      headers: [
        { text: 'Name', value: 'name', width: '1%' },
        {
          text: 'Description',
          value: 'description',
          filterable: false,
          width: '2%'
        },
        { text: 'File', value: 'filename', width: '1%' },
        {
          text: 'Edit or Delete',
          value: 'actions',
          sortable: false,
          align: 'center',
          width: '1%'
        }
      ],
      search: ''
    }
  },
  methods: {
    closeDialog() {
      this.dialog = false
    },
    deleteContainer(containerId) {
      this.deleteContainerId = containerId
      this.confirmDeleteDialog = true
    },
    async confirmDeleteContainer(containerId) {
      try {
        await this.$store.dispatch(
          'containers/deleteContainer',
          this.deleteContainerId
        )
        this.$toaster.toastSuccess('Container deleted!')
      } catch (e) {
        this.$toaster.toastError('Could not delete container')
      }
      this.confirmDeleteDialog = false
    },
    editContainer(containerId) {
      const containers = this.$store.state.containers.containers
      const containerToUpdate = containers.find(container => {
        return container.id === containerId
      })
      this.container.containerId = containerToUpdate.id
      this.container.containerName = containerToUpdate.name
      this.container.containerDescription = containerToUpdate.description
      this.container.containerIsInput = containerToUpdate.is_input_container?.toString()
      this.container.containerIsOutput = containerToUpdate.is_output_container?.toString()
      this.container.filename = containerToUpdate.filename
      this.dialog = true
    }
  },
  computed: {
    ...mapState('containers', ['containers']),
    items() {
      return this.$store.state.containers.containers
    }
  },
  created() {
    this.$store.dispatch('containers/fetchContainers')
  }
}
</script>
