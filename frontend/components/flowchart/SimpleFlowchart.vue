<template>
  <div>
    <v-icon-btn @click="savePipeline" icon="mdi-content-save" />
    <div
      class="flowchart-container"
      @mousemove="handleMove"
      @mouseup="handleUp"
      @mousedown="handleDown"
    >
      <svg width="100%" height="100%">
        <flowchart-link
          v-bind.sync="link"
          v-for="(link, index) in lines"
          :key="`link${index}`"
          @deleteLink="linkDelete(link.id)"
        ></flowchart-link>
      </svg>
      <flowchart-node
        v-bind.sync="node"
        v-for="(node, index) in scene.nodes"
        :key="`node${index}`"
        :options="nodeOptions"
        @linkingStart="linkingStart(node.id)"
        @linkingStop="linkingStop(node.id)"
        @nodeSelected="nodeSelected(node.id, $event)"
        @deleteNode="deleteNode(node.id)"
      >
      </flowchart-node>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import FlowchartLink from './FlowchartLink.vue'
import FlowchartNode from './FlowchartNode.vue'
import { getMousePosition } from './position'

export default {
  name: 'VueFlowchart',
  components: { FlowchartLink, FlowchartNode },
  props: {
    scene: {
      type: Object,
      default: () => ({
        centerX: 1024,
        scale: 1,
        centerY: 140,
        nodes: [],
        links: []
      })
    },
    height: {
      type: Number,
      default: 400
    },
    id: {
      type: Number
    }
  },
  data: () => ({
    action: {
      linking: false,
      dragging: false,
      scrolling: false,
      selected: 0
    },
    mouse: {
      x: 0,
      y: 0,
      lastX: 0,
      lastY: 0
    },
    draggingLink: null,
    rootDivOffset: {
      top: 0,
      left: 0
    }
  }),
  computed: {
    nodeOptions: ctx => ({
      centerY: ctx.scene.centerY,
      centerX: ctx.scene.centerX,
      scale: ctx.scene.scale,
      offsetTop: ctx.rootDivOffset.top,
      offsetLeft: ctx.rootDivOffset.left,
      selected: ctx.action.selected
    }),
    lines() {
      const lines = this.scene.links.map(link => {
        const fromNode = this.findNodeWithID(link.from)
        const toNode = this.findNodeWithID(link.to)
        let x, y, cy, cx, ex, ey
        x = this.scene.centerX + fromNode?.x
        y = this.scene.centerY + fromNode?.y
        ;[cx, cy] = this.getPortPosition('bottom', x, y)
        x = this.scene.centerX + toNode?.x
        y = this.scene.centerY + toNode?.y
        ;[ex, ey] = this.getPortPosition('top', x, y)
        return {
          start: [cx, cy],
          end: [ex, ey],
          id: link.id
        }
      })
      if (this.draggingLink) {
        let x, y, cy, cx
        const fromNode = this.findNodeWithID(this.draggingLink.from)
        x = this.scene.centerX + fromNode.x
        y = this.scene.centerY + fromNode.y
        ;[cx, cy] = this.getPortPosition('bottom', x, y)
        // push temp dragging link, mouse cursor postion = link end postion
        lines.push({
          start: [cx, cy],
          end: [this.draggingLink.mx, this.draggingLink.my]
        })
      }
      return lines
    }
  },
  mounted() {
    this.rootDivOffset.top = this.$el ? this.$el.offsetTop : 0
    this.rootDivOffset.left = this.$el ? this.$el.offsetLeft : 0
  },
  methods: {
    findNodeWithID(id) {
      return this.scene.nodes.find(item => id === item.id)
    },
    getPortPosition(type, x, y) {
      if (type === 'top') {
        return [x + 100, y]
      } else if (type === 'bottom') {
        return [x + 100, y + 170] // TODO: Make dynamic
      }
    },
    linkingStart(index) {
      this.action.linking = true
      this.draggingLink = {
        from: index,
        mx: 0,
        my: 0
      }
    },
    linkingStop(index) {
      // add new Link
      if (this.draggingLink && this.draggingLink.from !== index) {
        // check link existence
        const existed = this.scene.links.find(link => {
          return link.from === this.draggingLink.from && link.to === index
        })
        if (!existed) {
          let maxID = Math.max(
            0,
            ...this.scene.links.map(link => {
              return link.id
            })
          )
          const newLink = {
            id: maxID + 1,
            from: this.draggingLink.from,
            to: index
          }
          this.scene.links.push(newLink)
          this.$emit('linkAdded', newLink)
        }
      }
      this.draggingLink = null
    },
    linkDelete(id) {
      const deletedLink = this.scene.links.find(item => {
        return item.id === id
      })
      if (deletedLink) {
        this.scene.links = this.scene.links.filter(item => {
          return item.id !== id
        })
        this.$emit('linkBreak', deletedLink)
      }
    },
    nodeSelected(id, e) {
      this.action.dragging = id
      this.action.selected = id
      this.$emit('nodeClick', id)
      this.mouse.lastX =
        e.pageX || e.clientX + document.documentElement.scrollLeft
      this.mouse.lastY =
        e.pageY || e.clientY + document.documentElement.scrollTop
    },
    handleMove(e) {
      if (this.action.linking) {
        ;[this.mouse.x, this.mouse.y] = getMousePosition(this.$el, e)
        this.draggingLink.mx = this.mouse.x
        this.draggingLink.my = this.mouse.y
      }

      if (this.action.dragging) {
        this.mouse.x =
          e.pageX || e.clientX + document.documentElement.scrollLeft
        this.mouse.y = e.pageY || e.clientY + document.documentElement.scrollTop

        let diffX = this.mouse.x - this.mouse.lastX
        let diffY = this.mouse.y - this.mouse.lastY
        this.mouse.lastX = this.mouse.x
        this.mouse.lastY = this.mouse.y
        this.moveSelectedNode(diffX, diffY)
      }

      if (this.action.scrolling) {
        ;[this.mouse.x, this.mouse.y] = getMousePosition(this.$el, e)

        let diffX = this.mouse.x - this.mouse.lastX
        let diffY = this.mouse.y - this.mouse.lastY
        this.mouse.lastX = this.mouse.x
        this.mouse.lastY = this.mouse.y
        this.scene.centerX += diffX
        this.scene.centerY += diffY
      }
    },
    handleUp(e) {
      const target = e.target
      if (this.$el.contains(target)) {
        if (
          typeof target.className !== 'string' ||
          target.className.indexOf('node-input') < 0
        ) {
          this.draggingLink = null
        }
      }
      this.action.linking = false
      this.action.dragging = null
      this.action.scrolling = false
    },
    handleDown(e) {
      const target = e.target
      if (
        (target === this.$el || target.matches('svg, svg *')) &&
        e.which === 1
      ) {
        this.action.scrolling = true
        ;[this.mouse.lastX, this.mouse.lastY] = getMousePosition(this.$el, e)
        this.action.selected = null // deselectAll
      }

      this.$emit('canvasClick', e)
    },
    moveSelectedNode(dx, dy) {
      let index = this.scene.nodes.findIndex(
        item => item.id === this.action.dragging
      )
      let left = this.scene.nodes[index].x + dx / this.scene.scale
      let top = this.scene.nodes[index].y + dy / this.scene.scale

      this.$set(
        this.scene.nodes,
        index,
        Object.assign(this.scene.nodes[index], {
          x: left,
          y: top
        })
      )
    },
    deleteNode(id) {
      this.scene.nodes = this.scene.nodes.filter(node => node.id !== id)
      this.scene.links = this.scene.links.filter(
        link => link.from !== id && link.to !== id
      )
    },
    async saveNodesAndLinks() {
      const nodes = this.scene.nodes
      const links = this.scene.links
      var nodeArray = []
      var linkArray = []
      nodes.forEach(node => {
        const newPipelineNode = {
          node_id: node.id,
          container_id: node.container_id,
          x: node.x,
          y: node.y
        }
        nodeArray.push(newPipelineNode)
      })
      links.forEach(link => {
        const newPipelineLink = {
          to: link.to,
          from: link.from
        }
        linkArray.push(newPipelineLink)
      })
      const payload = {
        nodes: nodeArray,
        links: linkArray
      }
      const nodePath = `http://localhost:5000/pipeline/${this.id}/nodes`
      const linkPath = `http://localhost:5000/pipeline/${this.id}/links`

      await Promise.all([axios.delete(nodePath), axios.delete(linkPath)])

      //TODO: need to actually delete the PipelineNode and PipelineLinks for this pipeline before repopulating it
      const path = `http://localhost:5000/pipeline/${this.id}/`
      await axios.post(path, payload).catch(err => {
        console.log(err)
      })
    },
    savePipeline() {
      console.log('LINKS')
      console.log(this.scene.links)
      console.log('NODES')
      console.log(this.scene.nodes)
      this.saveNodesAndLinks()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.flowchart-container {
  margin: 0;
  width: 100%;
  height: calc(100vh - 24px);
  background: #ddd;
  position: relative;
  overflow: hidden;

  svg {
    cursor: grab;
  }
}
</style>
