<template>
  <v-card
    elevation="6"
    max-height="700"
    class="overflow-y-auto"
    :class="'dark'"
  >
    <v-card-header
      title="Your Containers"
      v-model="search"
      searchable
      searchLabel="Search by Name"
      icon="plus"
      :func="addContainerDialog"
    />
    <v-data-table
      id="Containers"
      :headers="headers"
      :items="items"
      :search="search"
    >
      <template v-slot:[`item.is_shared`]="{ item }">
        <v-simple-checkbox :value="item.is_shared" disabled />
      </template>
      <template v-slot:[`item.actions`]="{ item }">
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
        :isEditing="this.editing"
        :containerToEdit="this.container"
        :key="this.key"
        @closeDialog="closeDialog"
      />
    </v-dialog>
    <v-dialog
      v-model="confirmDeleteDialog"
      max-width="525px"
      min-height="600px"
    >
      <v-card class="overflow-x-hidden">
        <v-card-title style="word-break: break-word">
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
import { ContainerForm } from '~/components/container'
import VCardHeader from '../global/v-card-header.vue'

export default {
  name: 'ContainerList',
  components: {
    ContainerForm,
    VCardHeader
  },
  data: () => {
    return {
      editing: false,
      key: 0,
      deleteContainerId: null,
      dialog: false,
      confirmDeleteDialog: false,
      container: {
        containerId: '',
        filename: '',
        containerName: '',
        containerDescription: '',
        containerIsInput: false,
        containerIsOutput: false,
        containerTags: []
      },
      headers: [
        { text: 'Name', value: 'name', width: '20%' },
        {
          text: 'Description',
          value: 'description',
          filterable: false,
          width: '40%'
        },
        { text: 'Shared', value: 'is_shared', width: '10%' },
        { text: 'File', value: 'filename', width: '10%' },
        {
          text: 'Edit or Delete',
          value: 'actions',
          sortable: false,
          align: 'center',
          width: '20%'
        }
      ],
      search: ''
    }
  },
  computed: {
    ...mapState('containers', ['containers']),
    items() {
      return this.$store.getters['containers/userContainers']
    }
  },
  created() {
    this.$store.dispatch('containers/fetchContainers')
  },
  methods: {
    closeDialog() {
      this.dialog = false
    },
    addContainerDialog() {
      this.editing = false
      this.dialog = true
      this.key += 1
    },
    deleteContainer(containerId) {
      this.deleteContainerId = containerId
      this.confirmDeleteDialog = true
    },
    async confirmDeleteContainer() {
      await this.$store.dispatch(
        'containers/deleteContainer',
        this.deleteContainerId
      )
      this.confirmDeleteDialog = false
    },
    editContainer(containerId) {
      this.editing = true
      const containers = this.$store.state.containers.containers
      const containerToUpdate = containers.find(container => {
        return container.id === containerId
      })
      this.container.containerId = containerToUpdate.id
      this.container.containerName = containerToUpdate.name
      this.container.containerDescription = containerToUpdate.description
      this.container.containerIsInput = containerToUpdate.is_input_container?.toString()
      this.container.containerIsOutput = containerToUpdate.is_output_container?.toString()
      this.container.containerIsShared = containerToUpdate.is_shared?.toString()
      this.container.filename = containerToUpdate.filename
      this.container.containerTags = containerToUpdate.tags

      // force containerForm re-render
      this.key += 1
      this.dialog = true
    }
  }
}
</script>
