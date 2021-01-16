# Pipeline

## Creating a Pipeline

1. Go to the Pipelines :material-transit-connection-horizontal: page
2. Click :material-plus: and fill out the form
   You must provide a pipeline name
   You may provide an AE title if you would like this pipeline to automatically run upon receiving a specific DICOM instance
3. You will be brought to the pipeline-making canvas board
4. Click :material-arrow-expand-left: on the top left of the canvas to view your Containers
5. From the right-hand Container list, click :material-plus: on the Container card to add it to the canvas
6. Drag your Containers around to build your pipeline flow
7. Connect your Containers with the small nodes at the bottom and top of the cards
   The link between containers should start from a Container's bottom node to another Container's top node
8. If you would like your Pipeline results to be sent to another DICOM node, you can add the default **Dicom Output Container** to the end of your flow.
   To designate the DICOM node to send to, add the node's host and port and select it in the **Dicom Output Container**'s dropdown menu.
9. Click :material-content-save: to save your pipeline

## Editing a Pipeline

1. Go to the Pipelines :material-transit-connection-horizontal: page
2. Click the pipeline row that you want to view or edit
3. You can edit the Pipeline flow
   Edit the canvas board the same way you did so when first creating the Pipeline
   Delete Containers from the canvas with the :material-delete: on the Container card, and delete Container connections by hovering over the connection arrow and clicking the X
   Click :material-content-save: to save your changes
4. You can edit the Pipeline's info
   Click :material-information: on the top left
   Click :material-pencil: to edit your Pipeline's name, AE title, or shareability
   Click :material-content-save: to save your changes

---
