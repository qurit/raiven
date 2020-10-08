<template>
  <v-card elevation="6">
    <v-card-title>
      Your Containers
    </v-card-title>
    <v-card-text>
      <v-list v-for="container in containers" :key="container.id">
        {{ container }}
        <v-btn x-small color="blue" @click="editContainer(container.id)">
          Edit
        </v-btn>
        <v-btn x-small color="blue" @click="deleteContainer(container.id)">
          Delete
        </v-btn>
      </v-list>
    </v-card-text>
    <v-dialog v-model="dialog" max-width="900px" min-height="600px">
      <v-card>
        <v-form v-model="form">
          <v-col cols="12" md="12">
            <v-text-field
              v-model="containerName"
              label="Container name"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="12">
            <v-textarea
              v-model="containerDescription"
              label="Description"
              required
            ></v-textarea>
          </v-col>
          <v-row>
            <v-checkbox
              v-model="containerIsInput"
              label="Input"
              false-value="false"
              true-value="true"
              class="mx-10"
            />
            <v-checkbox
              v-model="containerIsOutput"
              label="Output"
              false-value="false"
              true-value="true"
              class="mx-10"
            />
          </v-row>
          <v-file-input
            v-model="file"
            label="Replace container file"
            @change="updateDockerFile"
          />
          <v-btn @click="submit"> Save </v-btn>
        </v-form>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  data: function() {
    return {
      currentFile: '',
      dialog: false,
      containerName: '',
      containerDescription: '',
      containerIsInput: false,
      containerIsOutput: false
    }
  },
  methods: {
    deleteContainer(containerId) {
      this.$store.dispatch('containers/deleteContainer', containerId)
    },
    editContainer(containerId) {
      const path = `http://localhost:5000/container/${containerId}`
      axios.get(path).then(res => {
        console.log(res.data)
        this.containerName = res.data.name
        this.containerDescription = res.data.description
        this.containerIsInput = res.data.is_input_container.toString()
        this.containerIsOutput = res.data.is_output_container.toString()
      })
      this.dialog = true
    }
  },
  computed: {
    ...mapState('containers', ['containers'])
  },
  created() {
    this.$store.dispatch('containers/fetchContainers')
  }
  // methods: {
  //   deleteContainer(container) {
  //     this.$store.commit('containers/delete', container)
  //   }
  // }
}
</script>
