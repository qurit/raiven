<template>
  <v-card elevation="10">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Build a Pipeline</b></v-toolbar-title>
    </v-toolbar>
    <v-card-subtitle>
      <b>Creating a Pipeline</b>
    </v-card-subtitle>
    <v-card-text>
      <ol>
        <li>
          Go to the <nuxt-link to="/pipeline">Pipelines</nuxt-link>
          <v-icon small color="icon">
            mdi-transit-connection-variant
          </v-icon>
          page
        </li>
        <li>
          Click <v-icon small color="icon">mdi-plus-</v-icon> and fill out the
          form
        </li>
        <li>
          Click <v-icon small color="icon">mdi-plus</v-icon> on the top left of
          the canvas to view your Containers
        </li>
        <li>
          Click <v-icon small color="icon">mdi-plus</v-icon> on the Container
          card to add that Container
        </li>
        <li>Drag your Containers around to build your pipeline flow</li>
        <li>
          Click <v-icon small color="icon">mdi-content-save </v-icon> to save
          your pipeline
        </li>
      </ol>
    </v-card-text>
    <v-card-subtitle>
      <b>Editing a Pipeline</b>
    </v-card-subtitle>
    <v-card-text>
      <ol>
        <li>
          Go to the <nuxt-link to="/pipeline">Pipelines</nuxt-link>
          <v-icon small color="#ffffff">
            mdi-transit-connection-variant
          </v-icon>
          page
        </li>
        <li>
          Click the pipeline row that you want to view or edit
        </li>
        <li>Make any necessary changes</li>
        <li>
          Click <v-icon small color="#ffffff">mdi-content-save</v-icon> to save
          your changes
        </li>
      </ol>
    </v-card-text>
  </v-card>
</template>
