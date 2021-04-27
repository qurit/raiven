# Pipelines

## Creating a Pipeline

1. Go to the _Pipelines_ :material-transit-connection-horizontal: page
2. Click :material-plus: and fill out the form
    * You must provide a Pipeline name
   You may provide an AE title if you would like this Pipeline to automatically run upon receiving a specific DICOM instance
3. You will be brought to the Pipeline creation canvas board
4. Click :material-arrow-expand-left: on the top left of the canvas to view your Containers
5. From the right-hand Container list, click :material-plus: on the Container card to add it to the canvas
6. Drag your Containers around to build your pipeline flow
7. Connect your Containers with the small nodes at left (input) and right (output) of the cards
     *   The link between Containers should start from a Container's right side node to another Container's left side
     *   While dragging the link, hover over the input node, and when it has changed colours, you can release the link to complete the connection.
8. If you would like your Pipeline results to be sent to another DICOM node, you can add the default **Dicom Output** Container to the end of your flow.
     * To designate the DICOM node to send to, add the node's host and port and select it in the **Dicom Output** Container's dropdown menu.
9. If you would like your Pipeline to receive from a DICOM node, you can add the default **Dicom Input** Container to the beginning of your flow.
     * To designate the DICOM node to receive from, add the node's host and port and select it in the **Dicom Input** Container's dropdown menu.
     *  You can set rules to decide when to run the Pipeline under specific conditions.
9. Click :material-content-save: to save your Pipeline

## Editing a Pipeline

1. Go to the _Pipelines_ :material-transit-connection-horizontal: page
2. Click the Pipeline row that you want to view or edit
3. You can edit the Pipeline flow
     * Edit the canvas board the same way you did so when first creating the Pipeline
     * Delete Containers from the canvas with the :material-delete: on the Container card, and delete Container connections by hovering over the connection arrow and clicking the X
     * Click :material-content-save: to save your changes
4. You can edit the Pipeline's info
     * Click :material-information: on the top left
     * Click :material-pencil: to edit your Pipeline's name, AE title, or shareability
     * Click :material-content-save: to save your changes

## Running a Pipeline

1. Go to the _Runs_ :material-play-outline: page
2. From the received DICOM instances, choose to send the Node :material-folder-network:, Patient :material-account: , Study :material-clipboard-list: , or Series to a Pipeline by clicking on the respective row
3. Select which pipeline you would like to send the images to
4. Click **Send** to start the Pipeline Run

## Viewing your Run Results

1. Go to the _Runs_ :material-play-outline: page
2. Navigate to the "Pipeline Run Results" table
3. Click :material-download: next to the repsective pipeline run to download the results as a zip file

## Viewing your files from Pipeline Runs

1. Go to the _Files_ :material-file-download-outline: page
2. Click :material-download: next to the respective file to download it

## Viewing a Pipeline's Runs

1. Go to the _Pipelines_ :material-transit-connection-horizontal: page
2. Click the pipeline row that you want to view
3. Click :material-information: on the top left to view this pipeline's runs
    * Information about a run's Containers and errors can be found here as well
