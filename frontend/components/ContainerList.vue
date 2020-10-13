<template>
  <v-card
    elevation="6"
    max-height="700"
    class="overflow-y-auto"
    :class="scrollbarTheme"
  >
    <v-card-title>
      Your Containers
    </v-card-title>
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
      <v-card class="overflow-x-hidden">
        <v-form v-model="form" class="ma-5">
          <v-col cols="12" md="12">
            <v-text-field
              v-model="containerName"
              label="Container name"
              :rules="[v => !!v || 'Container name is required']"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="12">
            <v-textarea
              v-model="containerDescription"
              label="Description"
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
            :label="fileName"
            @change="updateDockerFile"
            prepend-icon="mdi-docker"
          />
          <v-row justify="center">
            <v-btn @click="update" color="green"> Save </v-btn>
          </v-row>
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
      containerId: '',
      currentFile: '',
      dialog: false,
      containerName: '',
      containerDescription: '',
      containerIsInput: false,
      containerIsOutput: false
    }
  },
  methods: {
    readFile(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsArrayBuffer(file)
      })
    },
    deleteContainer(containerId) {
      this.$store.dispatch('containers/deleteContainer', containerId)
    },
    editContainer(containerId) {
      const path = `http://localhost:5000/container/${containerId}`
      axios.get(path).then(res => {
        console.log(res)
        this.containerId = res.data.id
        this.containerName = res.data.name
        this.containerDescription = res.data.description
        console.log(this.containerDescription)
        this.containerIsInput = res.data.is_input_container.toString()
        this.containerIsOutput = res.data.is_output_container.toString()
        this.fileName = res.data.filename
      })
      this.dialog = true
    },
    async update() {
      const config = { headers: { 'Content-Type': 'multipart/form-data' } }

      const formData = new FormData()
      formData.append('name', this.containerName)
      formData.append('dockerfile_path', 'blah')
      // console.log(JSON.parse(this.containerDescription))
      // formData.append('description', JSON.parse(this.containerDescription))
      formData.append('is_input_container', this.containerIsInput)
      formData.append('is_output_container', this.containerIsOutput)
      if (this.file) {
        const f = await this.readFile(this.file)
        formData.append('file', new Blob([f]))
        formData.append('filename', this.file.name)
      }
      if (this.containerDescription !== null) {
        formData.append('description', this.containerDescription)
      }

      const path = `http://localhost:5000/container/${this.containerId}/`
      await axios.put(path, formData).catch(err => {
        console.log(err)
      })
      this.$store.dispatch('containers/updateContainer')
      this.dialog = false
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
