<template>
  <v-card elevation="6">
    <!-- Edit an exiting container -->
    <div v-if="isEditing">
      <v-card-title>
        Edit your Container
      </v-card-title>
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
          :label="filename"
          @change="updateDockerFile"
          prepend-icon="mdi-docker"
        />
        <v-row justify="center">
          <v-btn @click="update" color="green">
            Save
          </v-btn>
        </v-row>
      </v-form>
    </div>
    <!-- Add a new container -->
    <div v-else>
      <v-card-title>
        Add a Container
      </v-card-title>
      <v-form v-model="form" ref="form">
        <v-container>
          <v-col cols="12" md="12">
            <v-text-field
              v-model="name"
              label="Container name*"
              :rules="[v => !!v || 'Container name is required']"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="12">
            <v-textarea v-model="description" label="Description"></v-textarea>
          </v-col>
          <v-row>
            <v-checkbox
              v-model="input"
              label="Input"
              false-value="0"
              true-value="1"
              class="mx-10"
            />
            <v-checkbox
              v-model="output"
              label="Output"
              false-value="0"
              true-value="1"
              class="mx-10"
            />
          </v-row>
          <v-file-input
            v-model="file"
            label="Upload a Dockerfile*"
            @change="updateDockerFile"
            :rules="[v => !!v || 'A Dockerfile is required']"
            required
            prepend-icon="mdi-docker"
          />
          <v-row justify="center">
            <v-btn :disabled="this.isDisabled" @click="submit" color="green">
              Add container
            </v-btn>
          </v-row>
        </v-container>
      </v-form>
    </div>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
  props: [
    'isEditing',
    'containerId',
    'containerName',
    'containerDescription',
    'containerIsInput',
    'containerIsOutput',
    'currentFile',
    'filename'
  ],
  data() {
    return {
      name: '',
      description: '',
      input: '0',
      output: '0',
      dockerFileName: '',
      file: ''
    }
  },
  methods: {
    test() {
      console.log(isEditing)
    },
    readFile(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsArrayBuffer(file)
      })
    },
    async updateDockerFile(file) {
      this.file = file
    },
    // submitting a new container
    async submit() {
      const config = { headers: { 'Content-Type': 'multipart/form-data' } }
      const f = await this.readFile(this.file)
      const formData = new FormData()
      formData.append('name', this.name)
      formData.append('dockerfile_path', 'blah')
      formData.append('description', this.description)
      formData.append('is_input_container', this.input)
      formData.append('is_output_container', this.output)
      formData.append('filename', this.file.name)
      formData.append('file', new Blob([f]))
      await this.$store.dispatch('containers/addContainer', formData)
      // this.$refs.form.reset()
      this.$emit('closeDialog')
    },
    // updating an existing container
    async update() {
      const config = { headers: { 'Content-Type': 'multipart/form-data' } }
      const formData = new FormData()
      formData.append('name', this.containerName)
      formData.append('dockerfile_path', 'blah')
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
      this.$store.dispatch('containers/updateContainer', {
        id: this.containerId,
        data: formData
      })
      this.$emit('closeDialog')
    }
  },
  computed: {
    isDisabled: function() {
      return !(this.name && this.file)
    }
  }
}
</script>
