<template>
  <div>
    <h1>Pipeline Maker Test</h1>
    <div class="tool-wrapper">
      <!-- <select v-model="newNodeType">
        <option
          v-for="(item, index) in nodeCategory"
          :key="index"
          :value="index"
          >{{ item }}</option
        >
      </select> -->
      <v-select
        v-model="newNodeType"
        :items="nodeCategory"
        item-text="title"
        item-value="id"
        key="id"
      >
      </v-select>
      <!-- <input
        type="text"
        v-model="newNodeLabel"
        placeholder="Input node label"
      /> -->
      <v-btn @click="addNode">Add Container</v-btn>
    </div>
    <SimpleFlowchart
      :scene.sync="scene"
      @nodeClick="nodeClick"
      @nodeDelete="nodeDelete"
      @linkBreak="linkBreak"
      @linkAdded="linkAdded"
      @canvasClick="canvasClick"
      :height="800"
    />
  </div>
</template>

<script>
import SimpleFlowchart from '~/components/flowchart/SimpleFlowchart'

export default {
  components: {
    SimpleFlowchart
  },
  data() {
    return {
      scene: {
        centerX: 1024,
        centerY: 140,
        scale: 1,
        nodes: [
          {
            id: 2,
            x: -700,
            y: -69,
            type: 'Action',
            label: 'test1'
          },
          {
            id: 4,
            x: -357,
            y: 80,
            type: 'Script',
            label: 'test2'
          },
          {
            id: 6,
            x: -557,
            y: 80,
            type: 'Rule',
            label: 'test3'
          }
        ],
        links: [
          {
            id: 3,
            from: 2, // node id the link start
            to: 4 // node id the link end
          }
        ]
      },
      newNodeType: 0,
      newNodeLabel: '',
      nodeCategory: this.$store.state.containers.containers
    }
  },
  methods: {
    canvasClick(e) {
      console.log('canvas Click, event:', e)
    },
    addNode() {
      let maxID = Math.max(
        0,
        ...this.scene.nodes.map(link => {
          return link.id
        })
      )
      this.scene.nodes.push({
        id: maxID + 1,
        x: -400,
        y: 50,
        type: this.nodeCategory[this.newNodeType - 1].title
      })
    },
    nodeClick(id) {
      console.log('node click', id)
      console.log(this.newNodeType)
    },
    nodeDelete(id) {
      console.log('node delete', id)
    },
    linkBreak(id) {
      console.log('link break', id)
    },
    linkAdded(link) {
      console.log('new link added:', link)
    }
  }
}
</script>
