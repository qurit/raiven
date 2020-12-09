<template>
  <v-card elevation="10">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Add a Container</b></v-toolbar-title>
    </v-toolbar>
    <v-card-subtitle>
      <b>Uploading a Container</b>
    </v-card-subtitle>
    <v-card-text>
      <ol type="1">
        <li>
          Go to the <nuxt-link to="/containers">Containers</nuxt-link>
          <v-icon small color="icon">
            mdi-package-variant-closed
          </v-icon>
          page
        </li>
        <li>Fill out the "Add a Container" form</li>
        <li>Click <v-btn x-small color="green" text>Add Container </v-btn></li>
      </ol>
    </v-card-text>
    <v-card-subtitle>
      <b>Editing a Container</b>
    </v-card-subtitle>
    <v-card-text>
      <ol type="1">
        <li>
          Go to the <nuxt-link to="/containers">Containers</nuxt-link>
          <v-icon small color="icon"> mdi-package-variant-closed </v-icon>
          page
        </li>
        <li>
          Click  <v-icon small color="icon"> mdi-pencil </v-icon> Edit</v-btn> next to the
          Container to be edited
        </li>
        <li>Edit the form</li>
        <li>Click <v-btn x-small color="green" text>Save Edits</v-btn></li>
      </ol>
    </v-card-text>
  </v-card>
</template>
