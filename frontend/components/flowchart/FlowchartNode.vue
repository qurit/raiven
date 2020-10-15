<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="flowchart-node"
      :style="nodeStyle"
      @mousedown="handleMousedown"
      v-bind:class="{ selected: options.selected === id }"
    >
      <v-sheet
        class="pa-2 title text-center poll-name"
        color="blue"
        height="170"
        width="200"
      >
        <v-expand-x-transition style="float: left">
          <v-icon-btn
            v-if="hover"
            delete
            color="red"
            @click="$emit('deleteNode')"
          />
        </v-expand-x-transition>
        {{ type }}
      </v-sheet>
      <FlowchartNodePort
        class="node-port node-input"
        @mouseup="$emit('linkingStop')"
      />
      <FlowchartNodePort
        class="node-port node-output"
        @mousedown="$emit('linkingStart')"
      />
    </v-card>
  </v-hover>
</template>

<script>
import FlowchartNodePort from './FlowchartNodePort.vue'
export default {
  name: 'FlowchartNode',
  components: { FlowchartNodePort },
  props: {
    id: undefined,
    x: 0,
    y: 0,
    type: undefined,
    options: {
      type: Object,
      default() {
        return {
          centerX: undefined,
          scale: undefined,
          centerY: undefined
        }
      }
    }
  },
  data: () => ({
    show: {
      delete: false
    }
  }),
  computed: {
    nodeStyle() {
      return {
        top: this.options.centerY + this.y * this.options.scale + 'px',
        left: this.options.centerX + this.x * this.options.scale + 'px',
        transform: `scale(${this.options.scale})`
      }
    }
  },
  methods: {
    handleMousedown(e) {
      // This could be removed with click.stop maybe?
      if (
        e.target.className.indexOf('node-input') < 0 &&
        e.target.className.indexOf('node-output') < 0
      ) {
        this.$emit('nodeSelected', e)
      }
      e.preventDefault()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.poll-name {
  overflow: hidden;
  text-overflow: ellipsis;
  // white-space: nowrap;
  word-wrap: break-word;
  // display: block;
  // line-height: 1em; /* a */
  // max-height: 2em; /* a x number of line to show (ex : 2 line)  */
}
.flowchart-node {
  margin: 0;
  width: 200px;
  height: 170px;
  position: absolute;
  box-sizing: border-box;
  z-index: 10;
  opacity: 0.9;
  cursor: move;
  transform-origin: top left;

  .node-port {
    position: absolute;
    left: 50%;
    transform: translate(-50%);
  }

  /* TODO: Make this dynamic sized */
  .node-input {
    top: -8px;
  }

  .node-output {
    bottom: -8px;
  }
}
</style>
