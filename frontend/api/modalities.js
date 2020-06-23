const URL = '/modalities'

export const getModalities = async ({ $axios }) =>
  (await $axios.get(URL)).data.modalities;
