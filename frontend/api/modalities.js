const URL = '/modalities'

export const getModalities = async ({ $axios }) =>
  (await $axios.get(URL)).data.modalities;

export const addModality = async ({ $axios, $toaster }, modality) => {
  try {
    const res = (await $axios.post(URL, modality));
    $toaster.toastSuccess("Modality Added")
    return res.data
  } catch (e) {
    $toaster.toastError("Modality Cant be Added")
  }
}
