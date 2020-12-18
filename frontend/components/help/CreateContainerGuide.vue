<template>
  <v-card elevation="10">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Create a Container</b></v-toolbar-title>
    </v-toolbar>
    <v-card-subtitle>
      <b>Creating a Container</b>
    </v-card-subtitle>
    <v-card-text>
      <ol type="1">
        <li>
          When creating a container, you should have a <b> Dockerfile </b> and
          your <b> main algorithm </b>
        </li>
        <li>
          The <b> Dockerfile </b> should resemble this example
          <v-icon-btn @click="dockerExample = true" info small />.
          <ul>
            <li>
              Install any dependencies you may require and set the environment
              variables to be <b> PICOM_INPUT_DIR /mnt/picom/input </b> and
              <b> PICOM_OUTPUT_DIR /mnt/picom/output</b>.
            </li>
          </ul>
          <ul>
            <li>
              Finally, write the instruction to run your
              <b> main algorithm </b> code.
            </li>
          </ul>
        </li>
        <li>
          The <b> main algorithm </b> should resemble this example
          <v-icon-btn @click="mainAlgorithmExample = true" info small />.
          <ul>
            <li>
              Map the <b> INPUT_DIR </b> to the previously defined
              <b> PICOM_INPUT_DIR </b> and the <b> OUTPUT_DIR </b> to the
              previously defined <b> PICOM_OUTPUT_DIR </b>
              <ul>
                <li>
                  Alternatively, if you did not set up the
                  <b> ENV </b> variables in the <b> Dockerfile </b>, then you
                  can set the <b> INPUT_DIR </b> to be
                  <b> /mnt/picom/input </b> and the <b> OUTPUT_DIR </b> to be
                  <b> /mnt/picom/output </b>.
                </li>
              </ul>
            </li>
          </ul>
          <ul>
            <li>
              Insert your DICOM processing algorithm.
            </li>
          </ul>
        </li>
        <li>
          Place both the <b> Dockerfile </b> and <b> main algorithm </b> in a
          zippped folder. You are now ready to move onto the next step,
          <b> Uploading a Container</b>!
        </li>
      </ol>
    </v-card-text>
    <v-dialog v-model="dockerExample" max-width="900">
      <v-img :src="require('@/static/docker-example.png')" />
    </v-dialog>
    <v-dialog v-model="mainAlgorithmExample" max-width="900">
      <v-img :src="require('@/static/main-algorithm-example.png')" />
    </v-dialog>
  </v-card>
</template>

<script>
import VIconBtn from '../global/v-icon-btn.vue'

export default {
  data() {
    return {
      dockerExample: false,
      mainAlgorithmExample: false
    }
  }
}
</script>
