<template>
  <v-form v-model="form">
    <v-container>
      <v-col cols="12" md="12">
        <v-text-field
          v-model="name"
          label="Container name"
          required
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="12">
        <v-textarea
          v-model="description"
          label="Description"
          required
        ></v-textarea>
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
      <v-file-input label="Upload new container" @change="updateDockerFile" />
      <v-btn @click="submit"> Add container </v-btn>
    </v-container>
  </v-form>
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
      dockerFileName: ''
    }
  },
  methods: {
    updateDockerFile(file) {
      console.log(file)
      this.dockerFileName = file.name
    },
    addContainer(payload) {
      const path = 'http://localhost:5000/container'
      axios.post(path, payload).catch(error => {
        console.log(error)
      })
    },
    submit() {
      console.log(this.dockerFileName)
      console.log(this.name)
      console.log(this.input)
      console.log(this.output)
      const payload = {
        // replace with current user
        user_id: '1',
        name: this.name,
        dockerfile_path: this.description,
        is_input_container: this.input,
        is_output_container: this.output
        // docker_file_name: this.dockerFileName
        // dockerfile_path: this.description
      }
      this.addContainer(payload)
    }
  }
}
</script>
