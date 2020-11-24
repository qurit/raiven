<template>
  <v-treeview
    dense
    :items="pipelineRuns"
    :loadChildren="loadChildren"
    hoverable
  >
    <template slot="label" slot-scope="{ item }">
      <!-- Pipeline Run -->
      <div v-if="item.hasOwnProperty('pipeline')">Run: {{ item.id }}</div>
      <!-- Pipeline Job  -->
      <div v-if="item.hasOwnProperty('pipeline_node_id')">
        Job: {{ item.id }}
      </div>
      <!-- Pipeline Job Error -->
      <div v-if="item.hasOwnProperty('pipeline_job_id')">
        Error: {{ item.stderr }}
      </div>
      <!-- Pipeline Node that was run for that job -->
      <div v-if="item.hasOwnProperty('container_id')" @click="test(item)">
        From Container: {{ item.container.name }}
      </div>
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
    loadChildren(item) {
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
        this.getJobErrors(item)
        this.getJobNode(item)
      }
    },
    getJobErrors(job) {
      const URL = `pipeline/job/${job.id}/errors`
      return generic_get(this, URL)
        .then(data => {
          data.forEach(studies => {
            job.children.push(studies)
          })
        })
        .catch(err => console.log(err))
    },
    getJobNode(job) {
      const URL = `pipeline/job/node/${job.pipeline_node_id}`
      return generic_get(this, URL)
        .then(data => {
          data.forEach(studies => {
            job.children.push(studies)
          })
        })
        .catch(err => console.log(err))
    }
  },
  created() {
    this.getInfo()
  }
}
</script>
