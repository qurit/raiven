<template>
  <v-card elevation="6">
    <v-card-header
      :title="isEditing ? 'Edit your Container' : 'Add a Container'"
    />
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
      <v-row align="center" class="mx-3">
        <v-combobox
          v-model="container.containerTags"
          :items="items"
          label="Select tags"
          multiple
          chips
          item-text="tag_name"
          item-value="tag_name"
          :return-object="false"
          deletable-chips
        >
        </v-combobox>
      </v-row>
      <v-row>
        <v-col md="9">
          <v-file-input
            v-model="file"
            :label="container.filename"
            @change="updateDockerFile"
            prepend-icon="mdi-docker"
          />
        </v-col>
        <v-col md="3">
          <v-checkbox
            v-model="container.containerIsShared"
            label="Shared"
            false-value="false"
            true-value="true"
          />
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-icon-btn
          save
          :disabled="isDisabled"
          @click="submit"
          color="confirm"
          class="ma-4"
        />
      </v-row>
    </v-form>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'ContainerForm',
  props: {
    isEditing: {
      type: Boolean
    },
    containerToEdit: {
      type: Object,
      default: () => {
        return undefined
      }
    }
  },
  data() {
    return {
      file: [],
      container: {
        containerId: '',
        filename: '',
        containerName: '',
        containerDescription: '',
        containerIsInput: false,
        containerIsOutput: false,
        containerIsShared: false,
        containerTags: []
      },
      containerToTag: null
    }
  },
  computed: {
    // disables button if no name or dockerfile for new container
    isDisabled: function() {
      return this.isEditing
        ? false
        : !(this.container.containerName && this.container.filename)
    },
    ...mapState('tags', ['tags']),
    items() {
      return this.$store.state.tags.tags
    }
  },
  created() {
    this.populate()
    this.$store.dispatch('tags/fetchTags')
  },
  methods: {
    populate() {
      if (this.isEditing && this.containerToEdit) {
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
        this.container.containerTags = []
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
      this.container.filename = file?.name
    },
    async submit() {
      const config = { headers: { 'Content-Type': 'multipart/form-data' } }
      const formData = new FormData()
      formData.append('name', this.container?.containerName)
      formData.append('is_input_container', this.container.containerIsInput)
      formData.append('is_output_container', this.container.containerIsOutput)
      formData.append('is_shared', this.container.containerIsShared)
      if (this.file instanceof Object && !(this.file instanceof Array)) {
        const f = await this.readFile(this.file)
        formData.append('file', new Blob([f]))
        formData.append('filename', this.file.name)
      }
      if (!!this.container.containerDescription) {
        formData.append('description', this.container.containerDescription)
      }
      if (!!this.isEditing && !!this.containerToEdit) {
        this.containerToTag = await this.$store.dispatch(
          'containers/updateContainer',
          {
            id: this.container.containerId,
            data: formData
          }
        )
        if (this.container.containerTags.length !== 0) {
          if (this.container.containerTags[0].hasOwnProperty('tag_name')) {
            const tagNameArray = this.container.containerTags.map(
              tag => tag.tag_name
            )
            await this.$store.dispatch('tags/addTag', tagNameArray)
            await this.$store.dispatch('tags/addContainerTags', {
              containerId: this.containerToTag?.id,
              tags: tagNameArray
            })
          } else {
            await this.$store.dispatch(
              'tags/addTag',
              this.container.containerTags
            )
            await this.$store.dispatch('tags/addContainerTags', {
              containerId: this.containerToTag?.id,
              tags: this.container.containerTags
            })
          }
        } else {
          await this.$store.dispatch('tags/addContainerTags', {
            containerId: this.containerToTag?.id,
            tags: []
          })
        }
      } else {
        this.containerToTag = await this.$store.dispatch(
          'containers/addContainer',
          formData
        )
        await this.$store.dispatch('tags/addTag', this.container.containerTags)
        await this.$store.dispatch('tags/addContainerTags', {
          containerId: this.containerToTag?.id,
          tags: this.container.containerTags
        })

        this.$refs.form.reset()
        this.container.containerIsInput = false
        this.container.containerIsOutput = false
        this.container.containerIsShared = false
      }
      this.$emit('closeDialog')
      await this.$store.dispatch('containers/fetchContainers')
    }
  }
}
</script>
