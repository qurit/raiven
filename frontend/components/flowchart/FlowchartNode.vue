<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="flowchart-node"
      :style="nodeStyle"
      @mousedown="handleMousedown"
      v-bind:class="{ selected: options.selected === id }"
      rounded
    >
      <!-- Input Port -->
      <FlowchartNodePort
        v-if="!container_is_input"
        class="node-port node-input"
        @mouseup="$emit('linkingStop')"
      />

      <!-- Node Data -->
      <v-card-title v-text="type" />
      <v-select
        v-if="container_is_output"
        :items="destinations"
        item-text="full_name"
        item-value="id"
        label="Destination"
        dense
        solo
        flat
      >
        <template v-slot:prepend-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                Add A Destination
              </v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-icon-btn add @click="destinationDialog = true" />
            </v-list-item-action>
          </v-list-item>
          <v-divider light />
        </template>
      </v-select>
      <v-card-actions style="position: absolute; bottom: 0; width: inherit">
        <v-chip
          small
          v-text="container_is_input ? 'Input' : 'Output'"
          :color="nodeColor"
        />
        <v-spacer />
        <v-icon-btn delete color="red" @click="$emit('deleteNode')" />
      </v-card-actions>

      <!-- Output Port -->
      <FlowchartNodePort
        v-if="!container_is_output"
        class="node-port node-output"
        @mousedown="$emit('linkingStart')"
      />
      <!-- Destination Dialogs -->
      <v-dialog
        v-model="destinationDialog"
        max-width="900px"
        min-height="600px"
        @closeDialog="destinationDialog = false"
      >
        <OutputDestinationForm />
      </v-dialog>
    </v-card>
  </v-hover>
</template>

<script>
import FlowchartNodePort from './FlowchartNodePort.vue'
import OutputDestinationForm from '~/components/OutputDestinationForm'
import { mapState } from 'vuex'

export default {
  name: 'FlowchartNode',
  components: { FlowchartNodePort, OutputDestinationForm },
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
    },
    colors: {
      type: Object,
      default: () => ({
        input: 'orange',
        output: 'purple',
        default: 'blue'
      })
    }
  },
  data: () => ({
    destinationDialog: false,
    show: {
      delete: false
    }
  }),
  computed: {
    ...mapState('destination', ['destinations']),
    nodeStyle() {
      return {
        top: this.options.centerY + this.y * this.options.scale + 'px',
        left: this.options.centerX + this.x * this.options.scale + 'px',
        transform: `scale(${this.options.scale})`
      }
    },
    nodeColor: ctx => {
      if (ctx.container_is_output) return ctx.colors.output
      else if (ctx.container_is_input) return ctx.colors.input
      else return ctx.colors.default
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
