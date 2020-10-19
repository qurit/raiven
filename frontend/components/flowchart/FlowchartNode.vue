<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="flowchart-node"
      :style="nodeStyle"
      @mousedown="handleMousedown"
      v-bind:class="{ selected: options.selected === id }"
    >
      <div v-if="container_is_input">
        <v-sheet
          class="pa-2 title text-center poll-name"
          color="orange"
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
          {{ type }} <br />
          INPUT CONTAINER
        </v-sheet>
        <FlowchartNodePort
          class="node-port node-output"
          @mousedown="$emit('linkingStart')"
        />
      </div>
      <div v-else-if="container_is_output">
        <v-sheet
          class="pa-2 title text-center poll-name"
          color="purple"
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
          {{ type }} <br />
          Destination:
          <v-select
            dense
            outlined
            filled
            class="mt-4"
            :items="destinations"
            item-text="full_name"
            item-value="id"
          >
          </v-select>
        </v-sheet>
        <FlowchartNodePort
          class="node-port node-input"
          @mouseup="$emit('linkingStop')"
        />
      </div>
      <div v-else>
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
          <div v-if="container_is_input">
            THIS IS AN INPUT CONTAINER
          </div>
        </v-sheet>
        <FlowchartNodePort
          class="node-port node-input"
          @mouseup="$emit('linkingStop')"
        />
        <FlowchartNodePort
          class="node-port node-output"
          @mousedown="$emit('linkingStart')"
        />
      </div>
    </v-card>
  </v-hover>
</template>

<script>
import FlowchartNodePort from './FlowchartNodePort.vue'
import { mapState } from 'vuex'

export default {
  name: 'FlowchartNode',
  components: { FlowchartNodePort },
  props: {
    id: undefined,
    x: 0,
    y: 0,
    type: undefined,
    container_is_input: undefined,
    container_is_output: undefined,
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
    },
    ...mapState('destination', ['destinations'])
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
  },
  created() {
    this.$store.dispatch('destination/fetchDestinations')
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.poll-name {
  overflow: hidden;
  text-overflow: ellipsis;
  word-wrap: break-word;
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
