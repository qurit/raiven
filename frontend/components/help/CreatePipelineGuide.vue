<template>
  <v-card elevation="10">
    <v-card-header title="Step 3: Build a Pipeline" />
    <v-card-subtitle>
      <b>Creating a Pipeline</b>
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
          Click <v-icon small color="icon">mdi-plus</v-icon> and fill out the
          form
          <ul>
            <li>
              You must provide a Pipeline name
            </li>
            <li>
              You may provide an AE title if you would like this pipeline to
              automatically run upon receiving a specific DICOM instance
            </li>
          </ul>
        </li>
        <li>
          You will be brought to the Pipeline creation canvas board
        </li>

        <li>
          Click <v-icon small color="icon">mdi-arrow-expand-left</v-icon> on the
          top left of the canvas to view your Containers
        </li>
        <li>
          From the right-hand Container list, click
          <v-icon small color="icon">mdi-plus</v-icon> on the Container card to
          add it to the canvas
        </li>
        <li>Drag your Containers around to build your pipeline flow</li>
        <li>
          Connect your Containers with the small nodes at the left (input) and
          right (output) of the cards
          <ul>
            <li>
              The link between Containers should start from a Container's right
              side node to another Container's left side
            </li>
            <li>
              While dragging the link, hover over the input node, and when it
              has changed colours, you can release the link to complete the
              connection.
            </li>
          </ul>
        </li>
        <li>
          If you would like your Pipeline results to be sent to another DICOM
          node, you can add the default <b>Dicom Output </b> Container to the
          end of your flow.
          <ul>
            <li>
              To designate the DICOM node to send to, add the node's host and
              port and select it in the <b> Dicom Output </b> Container's
              dropdown menu.
            </li>
          </ul>
        </li>
        <li>
          If you would like your Pipeline to receive from a DICOM node, you can
          add the default <b>Dicom Input </b> Container to the beginning of your
          flow.
          <ul>
            <li>
              To designate the DICOM node to receive from, add the node's host
              and port and select it in the <b> Dicom Input </b> Container's
              dropdown menu.
            </li>
          </ul>
          <ul>
            <li>
              You can set rules to decide when to run the Pipeline under
              specific conditions.
            </li>
          </ul>
        </li>
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
          <v-icon small color="icon">
            mdi-transit-connection-horizontal
          </v-icon>
          page
        </li>
        <li>
          Click the Pipeline row that you want to view or edit
        </li>
        <li>
          You can edit the Pipeline flow
          <ul>
            <li>
              Edit the canvas board the same way you did so when first creating
              the Pipeline
            </li>
            <li>
              Delete Containers from the canvas with the
              <v-icon small color="icon"> mdi-delete </v-icon> on the Container
              card, and delete Container connections by hovering over the
              connection arrow and clicking the X
            </li>
            <li>
              Click <v-icon small color="icon">mdi-content-save</v-icon> to save
              your changes
            </li>
          </ul>
        </li>
        <li>
          You can view/edit the Pipeline's info
          <ul>
            <li>
              Click <v-icon small color="icon">mdi-information</v-icon> on the
              top left
            </li>
            <li>
              Click <v-icon small color="icon">mdi-pencil</v-icon> to edit your
              Pipeline's name, AE title, or shareability
            </li>
            <li>
              Click <v-icon small color="icon">mdi-content-save</v-icon> to save
              your changes
            </li>
          </ul>
        </li>
      </ol>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'CreatePipelineGuide'
}
</script>
