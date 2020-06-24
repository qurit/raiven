const URL = '/modalities'

export const echo = async ({ $axios }, modality) => (await $axios.get(`${URL}/${modality._id}/echo`)).data
