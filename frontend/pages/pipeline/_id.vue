<template>
  <v-row class="pipeline-creator" no-gutters>
    <v-col cols="12">
      <v-row
        class="ma-2"
        style="position: absolute; z-index: 1;"
        no-gutters
        align="center"
      >
        <v-btn @click="containerList = !containerList" class="my-6" large icon>
          <v-icon
            large
            color="#373740"
            v-text="containerList ? 'mdi-minus' : 'mdi-plus'"
          />
        </v-btn>
      </v-row>
      <SimpleFlowchart :scene.sync="scene" :id="pipeline_id" />
      <v-navigation-drawer v-model="containerList" absolute right>
        <template v-slot:prepend>
          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title>Your containers</v-list-item-title>
              <v-btn class="mt-2">
                <nuxt-link to="/containers">
                  Add a Container
                </nuxt-link>
              </v-btn>
            </v-list-item-content>
          </v-list-item>
        </template>
        <v-divider />

        <!-- Containers of different types can be colored differently -->
        <v-hover
          v-for="container in containers"
          :key="container.id"
          v-slot:default="{ hover }"
        >
          <v-card class="ma-2 title" :color="hover ? 'orange' : ''">
            <v-card-title v-text="container.name" />
            <v-card-text>
              {{ container.description }}
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-icon-btn add @click="addNode(container)" />
            </v-card-actions>
          </v-card>
        </v-hover>
      </v-navigation-drawer>
    </v-col>
  </v-row>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

import SimpleFlowchart from '~/components/flowchart/SimpleFlowchart'
import VIconBtn from '../../components/global/v-icon-btn'

export default {
  components: {
    VIconBtn,
    SimpleFlowchart
  },
  data() {
    return {
      containerList: false,
      scene: {
        centerX: 1024,
        centerY: 140,
        scale: 1,
        nodes: [],
        links: []
      },
      pipeline_id: ''
    }
  },
  methods: {
    addNode(container) {
      let maxID = Math.max(0, ...this.scene.nodes.map(link => link.id))
      this.scene.nodes.push({
        id: maxID + 1,
        x: -400,
        y: 50,
        type: container.name,
        container_id: container.id
      })
    },
    getContainers() {
      this.$store.dispatch('containers/fetchContainers')
    },
    getPipelineNodes(nodes) {
      nodes.forEach(node => {
        console.log(node)
        const containerNode = {
          id: node.id,
          x: node.x_coord,
          y: node.y_coord,
          container_id: node.container_id,
          type: node.container.name,
          label: node.container.description
        }
        this.scene.nodes.push(containerNode)
      })
    },
    getPipelineLinks(links) {
      links.forEach(link => {
        const containerLink = {
          id: link.id,
          to: link.to_node_id,
          from: link.from_node_id
        }
        this.scene.links.push(containerLink)
      })
    },
    async getSavedPipeline() {
      // since only getting the pipeline here, didn't put it in the store
      const path = `http://localhost:5000/pipeline/${this.pipeline_id}`
      const { data } = await axios.get(path)
      const { nodes, links } = data
      this.getPipelineNodes(nodes)
      this.getPipelineLinks(links)
    }
  },
  computed: {
    ...mapState('containers', ['containers'])
  },
  created() {
    this.pipeline_id = this.$router.history.current.params.id
    this.getContainers()
    this.getSavedPipeline(this.pipeline_id)
  }
}
</script>
