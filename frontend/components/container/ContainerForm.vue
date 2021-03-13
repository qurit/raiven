<template>
  <v-card elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title>
        <b
          >{{ !!containerToEdit ? 'Edit your Container' : 'Add a Container' }}
        </b></v-toolbar-title
      >
    </v-toolbar>
    <v-divider light />
    <v-form class="ma-5" ref="form">
      <v-col cols="12" md="12">
        <v-text-field
          v-model="container.containerName"
          label="Container name"
          :rules="[v => !!v || 'Container name is required']"
          required
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="12">
        <v-textarea
          v-model="container.containerDescription"
          label="Description"
        ></v-textarea>
      </v-col>
      <v-row>
        <v-combobox
          v-model="container.tags"
          :items="items"
          label="Select a favorite activity or create a new one"
          multiple
          chips
          item-text="tag_name"
          item-value="tag_name"
          :return-object="false"
          :change="test"
        >
        </v-combobox>
        <v-checkbox
          v-model="container.containerIsInput"
          label="Input"
          false-value="false"
          true-value="true"
          class="mx-10"
        />
        <v-checkbox
          v-model="container.containerIsOutput"
          label="Output"
          false-value="false"
          true-value="true"
          class="mx-10"
        />
        <v-checkbox
          v-model="container.containerIsShared"
          label="Shared"
          false-value="false"
          true-value="true"
          class="mx-10"
        />
      </v-row>
      <v-file-input
        v-model="file"
        :label="container.filename"
        @change="updateDockerFile"
        prepend-icon="mdi-docker"
      />
      <v-row justify="center">
        <v-btn @click="submit" color="confirm" class="ma-4" text>
          {{ !!containerToEdit ? 'Save Edits' : 'Add Container' }}
        </v-btn>
      </v-row>
    </v-form>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
export default {
  props: {
    containerToEdit: {
      type: Object,
      default: () => {
        return undefined
      }
    }
  },
  data() {
    return {
      file: '',
      container: {
        containerId: '',
        filename: '',
        containerName: '',
        containerDescription: '',
        containerIsInput: false,
        containerIsOutput: false,
        containerIsShared: false
      },
      recentContainer: null
    }
  },
  created() {
    this.populate()
    this.$store.dispatch('tags/fetchTags')
  },
  computed: {
    // disables button if no name or dockerfile for new container
    isDisabled: function() {
      return !!this.containerToEdit
        ? false
        : !(this.container.containerName && this.file)
    },
    ...mapState('tags', ['tags']),
    items() {
      console.log(this.$store.state.tags)
      return this.$store.state.tags.tags
    }
  },
  methods: {
    populate() {
      if (!!this.containerToEdit) {
        // getting the values for the existing container
        this.container = JSON.parse(JSON.stringify(this.containerToEdit))
      } else {
        // default values for adding a new container
        this.container.containerId = ''
        this.container.filename = ''
        this.container.containerName = ''
        this.container.containerDescription = ''
        this.container.containerIsInput = false
        this.container.containerIsOutput = false
        this.container.containerIsShared = false
      }
    },
    readFile(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsArrayBuffer(file)
      })
    },
    updateDockerFile(file) {
      this.file = file
    },
    async submit() {
      console.log(this.container.tags)
      const config = { headers: { 'Content-Type': 'multipart/form-data' } }
      const formData = new FormData()
      formData.append('name', this.container?.containerName)
      formData.append('is_input_container', this.container.containerIsInput)
      formData.append('is_output_container', this.container.containerIsOutput)
      formData.append('is_shared', this.container.containerIsShared)
      if (this.file) {
        const f = await this.readFile(this.file)
        formData.append('file', new Blob([f]))
        formData.append('filename', this.file.name)
      }
      if (!!this.container.containerDescription) {
        formData.append('description', this.container.containerDescription)
      }
      if (!!this.containerToEdit) {
        const data = await this.$store.dispatch('containers/updateContainer', {
          id: this.container.containerId,
          data: formData
        })
        console.log('IN EDIT')
        console.log(data)
      } else {
        const data = await this.$store.dispatch(
          'containers/addContainer',
          formData
        )
        // .then(x => {
        //   // this.$refs.form.reset()
        //   this.container.containerIsInput = false
        //   this.container.containerIsOutput = false
        //   this.container.containerIsShared = false
        //   this.recentContainer = x
        // })
        console.log(data)
      }
      const recentlyAddedContainer = this.$store.getters[
        'containers/recentContainer'
      ]

      console.log('A;SLDFJASL;DFJASDL;JF')
      console.log(this.recentContainer)

      await this.$store.dispatch('tags/addTag', this.container.tags)

      // console.log(this.container.tags)
      // await this.$store.dispatch('tags/addContainerTags', {
      //   containerId: recentlyAddedContainer.id,
      //   tags: this.container.tags
      // })

      this.$emit('closeDialog')
      this.$toaster.toastSuccess('Container saved!')
    }
  }
}
</script>
