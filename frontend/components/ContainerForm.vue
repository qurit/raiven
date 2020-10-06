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
      <v-file-input
        v-model="file"
        label="Upload new container"
        @change="updateDockerFile"
      />
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
      dockerFileName: '',
      file: ''
    }
  },
  methods: {
    updateDockerFile(file) {
      console.log(file)
      // const test = JSON.stringify(file)
      // console.log(typeof file)
      // this.dockerFileName = file.name

      // const testing = new Blob([JSON.stringify(file)], {
      //   type: 'application/json'
      // })

      // console.log(testing)

      // const reader = new FileReader()
      // const test = reader.readAsText(testing, 'UTF-8')

      this.file = file
    },
    addContainer(payload) {
      console.log(payload)
      this.$store.dispatch('containers/addContainer', payload)
    },
    submit() {
      console.log(this.file)
      const payload = {
        user_id: '1',
        name: this.name,
        dockerfile_path: 'blah',
        description: this.description,
        is_input_container: this.input,
        is_output_container: this.output,
        dockerfile: this.file || 'No file'
      }
      this.addContainer(payload)
    }
  }
}
</script>
