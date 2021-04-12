<template>
  <v-card elevation="10">
    <v-card-header title="Step 1: Create a Container" />
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
          The <b> Dockerfile </b> should resemble
          <a
            href="https://raiven.qurit.ca/containers/#dockerfile-example"
            target="_blank"
          >
            this example
          </a>
          <ul>
            <li>
              Install any dependencies you may require and set the environment
              variables to be <b> PICOM_INPUT_DIR /mnt/picom/input </b> and
              <b> PICOM_OUTPUT_DIR /mnt/picom/output</b>
            </li>
          </ul>
          <ul>
            <li>
              Finally, write the instruction to run your
              <b> main algorithm </b> code
            </li>
          </ul>
        </li>
        <li>
          The <b> main algorithm </b> should resemble
          <a
            href="https://raiven.qurit.ca/containers/#algorithm-example"
            target="_blank"
          >
            this example
          </a>
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
                  <b> /mnt/picom/output </b>
                </li>
              </ul>
            </li>
          </ul>
          <ul>
            <li>
              Insert your DICOM processing algorithm
            </li>
          </ul>
        </li>
        <li>
          Place both the <b> Dockerfile </b> and <b> main algorithm </b> in a
          zippped folder
        </li>
      </ol>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'CreateContainerGuide'
}
</script>
