const URL = '/jobs'

export const getJobs = async ({ $axios }) => (await $axios.get(URL)).data.jobs

export const deleteAllJobs = async ({ $axios }) => (await $axios.delete(URL)).data

export const addJob = async ({ $axios }) => (await $axios.post(URL)).data
