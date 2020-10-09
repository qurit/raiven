<template>
  <v-card elevation="6">
    <v-card-title>
      Your Containers
    </v-card-title>
    <v-card-text>
      <v-list v-for="container in containers" :key="container.id">
        {{ container.name }}
        <v-btn x-small color="blue" @click="editContainer(container.id)">
          Edit
        </v-btn>
        <v-btn x-small color="red" @click="deleteContainer(container.id)">
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
          <v-col cols="12" md="12">
            <v-text>
              Upload a new file to replace the current file
            </v-text>
          </v-col>
          <v-file-input
            v-model="file"
            :label="fileName"
            @change="updateDockerFile"
          />
          <v-btn @click="update"> Save </v-btn>
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
      formData.append('description', this.containerDescription)
      formData.append('is_input_container', this.containerIsInput)
      formData.append('is_output_container', this.containerIsOutput)
      if (this.file) {
        const f = await this.readFile(this.file)
        formData.append('file', new Blob([f]))
        formData.append('filename', this.file.name)
      }

      const path = `http://localhost:5000/container/${this.containerId}/`
      await axios.put(path, formData).catch(err => {
        console.log(err)
      })
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
