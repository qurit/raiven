<template>
  <v-card elevation="10">
    <v-card-header title="Step 4: Run a Pipeline" />
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
          From the received DICOM instances, choose to send the Node
          <v-icon small color="icon">mdi-folder-network</v-icon>, Patient
          <v-icon small color="icon">mdi-account</v-icon>, Study
          <v-icon small color="icon">mdi-clipboard-list</v-icon>, or Series to a
          Pipeline by clicking on the respective row
        </li>
        <li>
          Select which pipeline you would like to send the images to
        </li>
        <li>
          Click <v-btn text x-small color="confirm"> Send </v-btn> to start the
          Pipeline Run
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
          Navigate to the "Pipeline Run Results" table
        </li>
        <li>
          Click <v-icon small color="icon">mdi-download</v-icon> next to the
          repsective pipeline run to download the results as a zip file
        </li>
      </ol>
    </v-card-text>
    <v-card-subtitle>
      <b>Viewing a Pipeline's Runs</b>
    </v-card-subtitle>
    <v-card-text>
      <ol>
        <li>
          Go to the <nuxt-link to="/pipeline">Pipelines</nuxt-link>
          <v-icon small color="icon">
            mdi-transit-connection-horizontal
          </v-icon>
          page
        </li>
        <li>
          Click the pipeline row that you want to view
        </li>
        <li>
          Click <v-icon small color="icon">mdi-information</v-icon> on the top
          left to view this pipeline's runs
          <ul>
            <li>
              Information about a run's containers and errors can be found here
              as well
            </li>
          </ul>
        </li>
      </ol>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'RunPipelineGuide'
}
</script>
