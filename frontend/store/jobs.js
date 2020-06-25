import { getJobs, addJob, deleteAllJobs } from "../api/job";

export const state = () => ({
  jobs: []
})

export const mutations = {
  setJobs: (state, jobs) => state.jobs = jobs,
  deleteAllJobs: (state) => state.jobs = [],
  addJob: (state, job) => state.jobs.push(job),
}

export const actions = {
  async fetchJobs({commit}) {
    commit('setJobs', await getJobs(this))
  },
  async addJob({commit}) {
    commit('addJob', await addJob(this))
  },
  async deleteAllJobs({commit}) {
    commit('deleteAllJobs', await deleteAllJobs(this))
  }
}
