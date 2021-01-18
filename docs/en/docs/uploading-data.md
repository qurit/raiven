
---

DICOM is the standard for the communication and management of medical images and related data. Raiven has built in support for AE's to upload DICOM data directly to a Raiven server and allows for three different options for pushing files. Which option you select is dictated by the <b>ae_title</b> you associate with when making the connection to the Raiven server. The available options are: pushing DICOM globally, pushing DICOM to a specific user, and pushing DICOM to a specific pipeline.

## Pushing DICOM globally

This option saves your DICOM data on the Raiven server and makes the data available to <b>all</b> users on the network. This option requires an <b>ae_title</b> of "RAIVEN". <b>Avoid</b> utilizing this option if your data contains private information.

## Pushing DICOM to a specific user

This option saves your DICOM data on the Raiven server but only makes the data available to a specific user. This option requires an <b>ae_title</b> of "RVU-{username}" where  "{username}" is replaced by the username of the account you wish to send data to. Use this option if your data contains private information that you do not want other users accessing. 

## Pushing DICOM to a specific pipeline

This option will immediately send your DICOM data to an existing pipeline on the Raiven server for processing. The DICOM files that you send in this manner will <b>not</b> be stored within the application and will eventually be deleted after the pipeline has finished processing it. Aditionally, one can configure the pipeline to send the resulting data directly back to the AE that sent it in. This option requires an <b>ae_title</b> of "RVP-{Pipeline AE Title}" where "{Pipeline AE Title}" is replaced by the ae title of the desired pipeline. The AE title of a pipeline can be configured in RAIVEN.
## Example code

Included in the project is an example SCP script in which you can test performing a C-Store within your desired Raiven instance. To do this, issue the following commands

<div class="termy">

```console
$ cd backend\tests\test_dicom
$ python .\test_scp.py
```
</div>

<b>Note</b> that you must first configure the UPLOAD_DIR and UPLOAD_AE_TITLE variables within the script prior to running the program. The UPLOAD_AE_TITLE will dictate what option is chosen for pushing the dicom data.

---

<p align="center">
  <em>Proudly Sponsored by <a href="https://qurit.ca">Qurit</a></em>
</p>
<p align="center">
  <img src="../assets/qurit-logo-text.png" alt="Qurit Logo" style="max-height: 100px" />
</p>

<!-- Abbreviations -->
*[DICOM]: Digital Imaging and Communications in Medicine
*[AE]: Application Entity
*[SCP]: Service Class Provider