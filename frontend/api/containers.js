const URL = 'containers'

export const getContainers = async ({ $axios }) => (await $axios.get(URL)).data.containers

export const scaleWorkers = async ({ $axios }, count) => (await $axios.post(`${URL}/workers`, { count }))
