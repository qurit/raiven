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
import axios from 'axios'
import { mapState } from 'vuex'
import ContainerForm from '../components/ContainerForm'

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
    deleteContainer(containerId) {
      this.$store.dispatch('containers/deleteContainer', containerId)
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

<style>
/* not sure if this should be defined in another style */
.dark::-webkit-scrollbar {
  width: 15px;
}

.dark::-webkit-scrollbar-track {
  background: #202020;
  border-left: 1px solid #2c2c2c;
}

.dark::-webkit-scrollbar-thumb {
  background: #3e3e3e;
  border: solid 3px #252525;
  border-radius: 7px;
}

.dark::-webkit-scrollbar-thumb:hover {
  background: #808080;
}
</style>
