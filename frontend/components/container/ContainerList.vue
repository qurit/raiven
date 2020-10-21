<template>
  <v-card
    elevation="6"
    max-height="700"
    class="overflow-y-auto"
    :class="'dark'"
  >
    <v-card-title>
      Your Containers
    </v-card-title>
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
      dialog: false,
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
    async deleteContainer(containerId) {
      await this.$store.dispatch('containers/deleteContainer', containerId)
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
