<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="flowchart-node"
      :style="nodeStyle"
      @mousedown="handleMousedown"
      v-bind:class="{ selected: options.selected === id }"
    >
      <v-sheet class="pa-4 title text-center" color="info" height="170" width="200">
        {{ type }}
        <v-expand-x-transition style="float: right">
        <v-icon-btn v-if="hover" delete color="tertiary" @click="$emit('deleteNode')"/>
      </v-expand-x-transition>
      </v-sheet>
      <FlowchartNodePort class="node-port node-input" @mouseup="$emit('linkingStop')"/>
      <FlowchartNodePort class="node-port node-output" @mousedown="$emit('linkingStart')"/>


    </v-card>
  </v-hover>
</template>

<script>
  import FlowchartNodePort from './FlowchartNodePort.vue'
  export default {
    name: 'FlowchartNode',
    components: {FlowchartNodePort},
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
        if (e.target.className.indexOf('node-input') < 0 && e.target.className.indexOf('node-output') < 0) {
          this.$emit('nodeSelected', e)
        }
        e.preventDefault()
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
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
