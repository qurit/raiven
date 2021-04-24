<template>
  <div>
    <v-treeview
      dense
      :items="pipelineRuns"
      :loadChildren="loadChildren"
      hoverable
    >
      <template v-slot:prepend="{ item }">
        <v-icon v-if="item.icon" v-text="item.icon"></v-icon>
      </template>
      <template slot="label" slot-scope="{ item }">
        <!-- Pipeline Run -->
        <div v-if="item.hasOwnProperty('pipeline')">Run: {{ item.id }}</div>
        <!-- Pipeline Job  -->
        <div v-if="item.hasOwnProperty('pipeline_node_id')">
          Job: {{ item.id }}
        </div>
        <!-- Pipeline Job Error -->

        <a v-if="item.hasOwnProperty('stderr')" @click="openErrorMessage(item)">
          <v-tooltip right>
            <template v-slot:activator="{ on, attrs }">
              <span v-bind="attrs" v-on="on">Error </span>
            </template>
            <span>{{ tooltipInfo }}</span>
          </v-tooltip>
        </a>

        <!-- Pipeline Node that was run for that job -->
        <a
          v-if="item.hasOwnProperty('container_id')"
          @click="openContainerInfo(item)"
        >
          <v-tooltip right>
            <template v-slot:activator="{ on, attrs }">
              <span v-bind="attrs" v-on="on">
                Container: {{ item.container.name }}</span
              >
            </template>
            <span>{{ tooltipInfo }}</span>
          </v-tooltip>
        </a>
      </template>
    </v-treeview>

    <v-dialog v-model="errorDialog" max-width="1000px" min-height="700px">
      <ErrorInfo :error="this.error" />
    </v-dialog>

    <v-dialog v-model="containerDialog" max-width="1000px" min-height="700px">
      <ContainerInfo :node="this.node" />
    </v-dialog>
  </div>
</template>

<script>
import { generic_get } from '~/api'
import ErrorInfo from './ErrorInfo'
import ContainerInfo from './ContainerInfo'
export default {
  name: 'PipelineTreeviewInfo',
  components: { ErrorInfo, ContainerInfo },
  props: {
    pipelineId: {
      type: Number
    }
  },
  data: () => {
    return {
      pipelineRuns: [],
      errorDialog: false,
      containerDialog: false,
      error: '',
      node: '',
      tooltipInfo: 'Click for more info'
    }
  },
  created() {
    this.getInfo()
  },
  methods: {
    openErrorMessage(error) {
      this.error = error
      this.errorDialog = true
    },
    openContainerInfo(node) {
      this.node = node
      this.containerDialog = true
    },
    async getInfo() {
      const URL = `/pipeline/${this.pipelineId}/results`
      await generic_get(this, URL)
        .then(data => {
          this.pipelineRuns = data
        })
        .then(() => {
          this.pipelineRuns.forEach(pipelineRun => {
            this.$set(pipelineRun, 'children', [])
            this.$set(pipelineRun, 'icon', 'mdi-play-outline')
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
              job.icon = 'mdi-briefcase-outline'
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
        this.getJobNode(item)
        this.getJobErrors(item)
      }
    },
    async getJobErrors(job) {
      const URL = `pipeline/job/${job.id}/errors`
      try {
        const errors = await generic_get(this, URL)
        errors.forEach(error => {
          error.icon = 'mdi-alert-circle-outline'
          job.children.push(error)
        })
      } catch (e) {
        this.$toaster.toastError('Could not fetch errors')
      }
    },
    async getJobNode(job) {
      const URL = `pipeline/job/node/${job.pipeline_node_id}`
      try {
        const data = await generic_get(this, URL)
        data.forEach(node => {
          node.icon = 'mdi-package-variant-closed'
          job.children.push(node)
        })
      } catch (e) {
        this.$toaster.toastError('Could not fetch errors')
      }
    }
  }
}
</script>
