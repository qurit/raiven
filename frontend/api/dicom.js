const URL = '/dicom'

export const echo = async ({ $axios, $toaster }, modality) => {
  try {
   return (await $axios.get(`${URL}/echo/${modality._id}`)).data
  } catch (e) {
    $toaster.toastError('Not Implemented Yet')
  }
}
