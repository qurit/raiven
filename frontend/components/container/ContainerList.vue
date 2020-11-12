<template>
  <v-card
    elevation="6"
    max-height="700"
    class="overflow-y-auto"
    :class="'dark'"
  >
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Your Containers</b></v-toolbar-title>
    </v-toolbar>
    <v-divider light />
    <v-card-text>
      <v-list-item v-for="container in containers" :key="container.id">
        <v-col cols="8">
          <v-list-item-title>
            {{ container.name }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ container.description }}
          </v-list-item-subtitle>
        </v-col>
        <v-col cols="4">
          <v-btn small color="blue" @click="editContainer(container.id)">
            Edit
          </v-btn>
          <v-btn
            small
            color="red"
            @click="deleteContainer(container.id)"
            class="mx-2"
          >
            Delete
          </v-btn>
        </v-col>
      </v-list-item>
    </v-card-text>
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
      persistent
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
        <v-row justify="center" align="center">
          <v-btn class="ma-2" @click="confirmDeleteContainer"> Yes </v-btn>
          <v-btn @click="confirmDeleteDialog = false"> No </v-btn>
        </v-row>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import ContainerForm from '~/components/container/ContainerForm'

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
      }
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
      await this.$store.dispatch(
        'containers/deleteContainer',
        this.deleteContainerId
      )
      this.confirmDeleteDialog = false
      this.$toaster.toastSuccess('Container deleted!')
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
    ...mapState('containers', ['containers'])
  },
  created() {
    this.$store.dispatch('containers/fetchContainers')
  }
}
</script>
