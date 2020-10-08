<template>
  <v-card elevation="6">
    <v-form v-model="form">
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
          label="Upload new container*"
          @change="updateDockerFile"
          :rules="[v => !!v || 'Dockerfile is required']"
          required
        />
        <v-btn :disabled="this.isDisabled" @click="submit">
          Add container
        </v-btn>
      </v-container>
    </v-form>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
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
    addContainer(payload) {
      this.$store.dispatch('containers/addContainer', payload)
    },
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
      this.addContainer(formData)
    }
  },
  computed: {
    isDisabled: function() {
      return !(this.name && this.file)
    }
  }
}
</script>
