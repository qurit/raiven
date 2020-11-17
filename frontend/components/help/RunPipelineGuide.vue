<template>
  <v-card elevation="10">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Run Pipeline Guide</b></v-toolbar-title>
    </v-toolbar>
    <v-card-subtitle>
      <b>Running a Pipeline</b>
    </v-card-subtitle>
    <v-card-text>
      <ol type="1">
        <li>
          Go to the <nuxt-link to="/runs">Runs</nuxt-link>
          <v-icon small color="icon">mdi-air-filter</v-icon> page
        </li>
        <li>
          From the list of received DICOM series, choose to send the Node
          <v-icon small color="icon">mdi-folder-network</v-icon>, Patient
          <v-icon small color="icon">mdi-account</v-icon>, Study
          <v-icon small color="icon">mdi-clipboard-list</v-icon>, or Series to a
          Pipeline by clicking on the respective row
        </li>
      </ol>
    </v-card-text>
    <v-card-subtitle>
      <b>Viewing your run results</b>
    </v-card-subtitle>
    <v-card-text>
      <ol type="1">
        <li>
          Go to the <nuxt-link to="/runs">Runs</nuxt-link>
          <v-icon small color="icon">mdi-air-filter</v-icon> page
        </li>
        <li>
          Navigate to the Pipeline Run Results table
        </li>
        <li>
          Click the download button
          <v-icon small color="icon">mdi-download</v-icon> next to the
          repsective pipeline run
        </li>
      </ol>
    </v-card-text>
  </v-card>
</template>
