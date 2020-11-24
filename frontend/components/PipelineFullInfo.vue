<template>
  <v-treeview
    dense
    :items="pipelineRuns"
    :loadChildren="loadChildren"
    hoverable
  >
    <template slot="label" slot-scope="{ item }">
      <!-- Pipeline Run -->
      <a v-if="item.hasOwnProperty('pipeline')"> Run: {{ item.id }} </a>
      <!-- Pipeline Job  -->
      <a v-if="item.hasOwnProperty('pipeline_node_id')"> Job: {{ item }} </a>
      <!-- Pipeline Job Error -->
      <a v-if="item.hasOwnProperty('pipeline_job_id')"> Errors: {{ item }} </a>
    </template>
  </v-treeview>
</template>

<script>
import { generic_get } from '~/api'
export default {
  props: {
    pipelineId: {
      type: Number
    }
  },
  data: () => {
    return {
      pipelineRuns: []
    }
  },
  methods: {
    async getInfo() {
      console.log('yes')
      const URL = `/pipeline/${this.pipelineId}/results`
      await generic_get(this, URL)
        .then(data => {
          this.pipelineRuns = data
        })
        .then(() => {
          this.pipelineRuns.forEach(pipelineRun => {
            this.$set(pipelineRun, 'children', [])
          })
        })
    },
    async loadChildren(item) {
      console.log(item)
      if (item.hasOwnProperty('pipeline')) {
        const URL = `/pipeline/run/${item.id}/jobs`
        return generic_get(this, URL)
          .then(data => {
            data.forEach(job => {
              job['children'] = []
            })
            return data
          })
          .then(jobs => {
            jobs.forEach(job => {
              item.children.push(job)
            })
          })
          .catch(err => console.log(err))
      }
      if (item.hasOwnProperty('pipeline_node_id')) {
        const URL = `pipeline/job/${item.id}/errors`
        return generic_get(this, URL)
          .then(data => {
            data.forEach(studies => {
              item.children.push(studies)
            })
          })
          .catch(err => console.log(err))
      }
    }
  },
  created() {
    this.getInfo()
  }
}
</script>
