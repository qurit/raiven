<template>
  <v-card elevation="10" width="1000">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title>Help Guide</v-toolbar-title>
    </v-toolbar>
    <v-divider light />
    <v-card-subtitle>
      <b>Uploading a Container</b>
    </v-card-subtitle>
    <v-card-text>
      1. Go to the <nuxt-link to="/containers">Containers</nuxt-link> page
      <br />
      2. Fill out the "Add a Container" form <br />
      3. Click <v-btn x-small color="green">Add Container</v-btn>
    </v-card-text>
    <v-card-subtitle>
      <b>Editing a Container</b>
    </v-card-subtitle>
    <v-card-text>
      1. Go to the <nuxt-link to="/containers">Containers</nuxt-link> page
      <br />
      2. Click <v-btn x-small color="blue">Edit</v-btn> next to the Container to
      be edited<br />
      3. Edit the form<br />
      4. Click <v-btn x-small color="green">Save</v-btn>
    </v-card-text>
    <v-divider light />
    <v-card-subtitle>
      <b>Building a Pipeline</b>
    </v-card-subtitle>
    <v-card-text>
      1. Go to the <nuxt-link to="/pipeline">Pipelines</nuxt-link> page <br />
      2. Click "Add Pipeline" <br />
      3. Click the "+" icon to view your containers <br />
      4. Drag your containers around to build your pipeline flow<br />
      5. Click <v-btn x-small color="green">Save Pipeline</v-btn>
    </v-card-text>
    <v-card-subtitle>
      <b>Editing a Pipeline</b>
    </v-card-subtitle>
    <v-card-text>
      1. Go to the <nuxt-link to="/pipeline">Pipelines</nuxt-link> page <br />
      2. Click <v-btn x-small color="blue">View</v-btn> next to the Pipeline to
      be edited <br />
      3. Make any necessary changes <br />
      5. Click <v-btn x-small color="green">Save Pipeline</v-btn> <br />
    </v-card-text>
    <v-card-subtitle>
      <b>Running a Pipeline</b>
    </v-card-subtitle>
    <v-card-text>
      <!-- //TODO: to determine -->
      1. Select a DICOM file to be run?
    </v-card-text>
  </v-card>
</template>
