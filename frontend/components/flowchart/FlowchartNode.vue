<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="flowchart-node"
      :style="nodeStyle"
      @mousedown="handleMousedown"
      @mouseover="handleMouseOver"
      @mouseleave="handleMouseLeave"
      v-bind:class="{ selected: options.selected === id }"
    >
      <v-sheet color="info">
        {{ type }}
      </v-sheet>

      <!-- Input Node  -->
      <div
        class="node-port node-input"
        @mousedown="inputMouseDown"
        @mouseup="inputMouseUp"
      />

      <!-- output Node  -->
      <div
        class="node-port node-output"
        @mousedown="outputMouseDown"
      />

      <v-expand-x-transition>
        <v-icon-btn v-if="hover" delete color="tertiary" @click="$emit('deleteNode', id)"/>
      </v-expand-x-transition>
      <v-sheet color="secondary">Output</v-sheet>
    </v-card>
  </v-hover>
</template>

<script>
  export default {
    name: 'FlowchartNode',
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
          top: this.options.centerY + this.y * this.options.scale + 'px', // remove: this.options.offsetTop +
          left: this.options.centerX + this.x * this.options.scale + 'px', // remove: this.options.offsetLeft +
          transform: `scale(${this.options.scale})`
        }
      }
    },
    methods: {
      handleMousedown(e) {
        const target = e.target || e.srcElement
        if (target.className.indexOf('node-input') < 0 && target.className.indexOf('node-output') < 0) {
          this.$emit('nodeSelected', e)
        }
        e.preventDefault()
      },
      handleMouseOver() {
        this.show.delete = true
      },
      handleMouseLeave() {
        this.show.delete = false
      },
      outputMouseDown(e) {
        this.$emit('linkingStart')
        e.preventDefault()
      },
      inputMouseDown(e) {
        e.preventDefault()
      },
      inputMouseUp(e) {
        this.$emit('linkingStop')
        e.preventDefault()
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  $themeColor: #ffcf44;
  $portSize: 12;
  .flowchart-node {
    margin: 0;
    width: 80px;
    height: 80px;
    position: absolute;
    box-sizing: border-box;
    border: none;
    background: blue;
    z-index: 10;
    opacity: 0.9;
    cursor: move;
    transform-origin: top left;

    .node-main {
      text-align: center;

      .node-type {
        background: $themeColor;
        color: black;
        font-size: 13px;
        padding: 6px;
      }

      .node-label {
        font-size: 13px;
      }
    }

    .node-port {
      position: absolute;
      width: #{$portSize}px;
      height: #{$portSize}px;
      left: 50%;
      transform: translate(-50%);
      border: 1px solid #ccc;
      border-radius: 100px;
      background: purple;

      &:hover {
        background: $themeColor;
        border: 1px solid $themeColor;
      }
    }

    .node-input {
      top: #{-2 + $portSize/-2}px;
    }

    .node-output {
      bottom: #{-2 + $portSize/-2}px;
    }
  }
</style>
