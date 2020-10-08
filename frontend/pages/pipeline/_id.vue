<template>
  <v-row class="pipeline-creator" no-gutters>
    <!--    <v-col cols="12">-->
    <!--        <h1>Pipeline Maker Test</h1>-->
    <!--    <div class="tool-wrapper">-->
    <!--      &lt;!&ndash; <select v-model="newNodeType">-->
    <!--        <option-->
    <!--          v-for="(item, index) in nodeCategory"-->
    <!--          :key="index"-->
    <!--          :value="index"-->
    <!--          >{{ item }}</option-->
    <!--        >-->
    <!--      </select> &ndash;&gt;-->
    <!--      <v-select-->
    <!--        v-model="newNodeType"-->
    <!--        :items="nodeCategory"-->
    <!--        item-text="title"-->
    <!--        item-value="id"-->
    <!--        key="id"-->
    <!--      >-->
    <!--      </v-select>-->
    <!--      &lt;!&ndash; <input-->
    <!--        type="text"-->
    <!--        v-model="newNodeLabel"-->
    <!--        placeholder="Input node label"-->
    <!--      /> &ndash;&gt;-->
    <!--      <v-btn @click="addNode">Add Container</v-btn>-->
    <!--    </div>-->
    <!--    </v-col>-->

    <v-col cols="12">
      <v-row
        class="ma-2"
        style="position: absolute; z-index: 1;"
        no-gutters
        align="center"
      >
        <v-btn class="ml-2" large icon>
          <v-icon large color="#373740" v-text="'mdi-content-save'" />
        </v-btn>
        <v-btn @click="containerList = !containerList" class="ml-2" large icon>
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
              <v-list-item-title>Containers</v-list-item-title>
              <v-list-item-subtitle
                >A list of all the containers</v-list-item-subtitle
              >
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
    getContainerNodes(currentPpelineId) {
      const path = `http://localhost:5000/pipeline/${this.pipeline_id}/nodes`
      axios.get(path).then(res => {
        res.data.forEach(test => {
          console.log(test)
          const containerNode = {
            id: test.id,
            x: test.x_coord,
            y: test.y_coord,
            container_id: test.container_id
          }
          console.log(containerNode)
          this.scene.nodes.push(containerNode)
        })
      })
    },
    getContainerLinks() {
      const path = `http://localhost:5000/pipeline/${this.pipeline_id}/links`
      axios.get(path).then(res => {
        res.data.forEach(test => {
          console.log(test)
          // TODO: should we actually save the node ids as well, so that we know the containers but also the nodes properly?
          const containerLink = {
            id: test.id,
            to: test.to_node_id,
            from: test.from_node_id
          }
          this.scene.links.push(containerLink)
        })
        console.log(this.scene.links)
      })
    },
    getSavedPipeline() {
      this.getContainerNodes()
      this.getContainerLinks()
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
