<template>
  <div>
    <v-card>
      *** IN PROGRESS: As a researcher, I would like to save the pipelines I
      have created ***
      <v-card-title>
        Pipeline Title here
      </v-card-title>
      <!-- See if editable state of the drag and drop thing is even doable -->
      <v-switch color="info" inset label="Edit" />
      <v-card-text>
        insert Saved pipeline here with the containers / saved drag and drop
        thing
      </v-card-text>
      <!-- if not in edit mode, then Save Changes button will be disabled -->
      <v-btn>
        Save changes
      </v-btn>
    </v-card>
    <v-divider />
    <v-card>
      Choose a Store Event to run your pipeline
      <!-- <v-file-input label="Upload your DICOM file" /> -->
      <v-select :items="files" item-text="name" item-value="name" multiple />

      <v-btn color="primary" @click="showSnackbar">
        Run pipeline!
      </v-btn>
    </v-card>
    <v-snackbar v-model="snackbar">
      Your pipeline is now running!
    </v-snackbar>
  </div>
</template>

<script>
import { files } from 'vuex'

export default {
  data: function() {
    return {
      snackbar: false,
      files: this.$store.state.files.files
    }
  },
  methods: {
    showSnackbar() {
      this.snackbar = true
    }
  }
}
</script>
