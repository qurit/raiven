<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="flowchart-node"
      :style="nodeStyle"
      @mousedown="handleMousedown"
      v-bind:class="{ selected: options.selected === id }"
      rounded
      :loading="loading"
    >
      <!-- Input Port -->
      <FlowchartNodePort
        v-if="!container_is_input"
        class="node-port node-input"
        @mouseup="$emit('linkingStop')"
      />

      <!-- Node Data -->
      <v-card-title style="word-break: break-word">
        {{ type }}
        <v-icon-btn
          v-if="selected"
          :icon="echoIcon"
          @click="sendEcho(selected)"
        />
      </v-card-title>
      <v-select
        v-if="container_is_output"
        v-model="selected"
        :items="destinations"
        item-text="title"
        item-value="id"
        label="Application Entity"
        dense
        solo
        flat
        return-object
        @change="changeDestination(selected)"
      >
        <template v-slot:prepend-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                Add A Destination
              </v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-icon-btn add @click="$emit('showDestinationForm')" />
            </v-list-item-action>
          </v-list-item>
          <v-divider light />
        </template>
      </v-select>
      <v-card-actions style="position: absolute; bottom: 0; width: inherit">
        <v-chip
          v-if="container_is_input"
          small
          v-text="'Input'"
          :color="nodeColor"
        />
        <v-chip
          v-if="container_is_output"
          small
          v-text="'Output'"
          :color="nodeColor"
        />
        <v-spacer />
        <v-icon-btn
          v-if="canEdit"
          delete
          color="cancel"
          @click="$emit('deleteNode')"
        />
      </v-card-actions>

      <!-- Output Port -->
      <FlowchartNodePort
        v-if="!container_is_output"
        class="node-port node-output"
        @mousedown="$emit('linkingStart')"
      />
    </v-card>
  </v-hover>
</template>

<script>
import echoMixin from "@/utilities/echoMixin";
import FlowchartNodePort from './FlowchartNodePort.vue'
import OutputDestinationForm from './OutputDestinationForm'
import { mapState } from 'vuex'

export default {
  name: 'FlowchartNode',
  components: { FlowchartNodePort, OutputDestinationForm },
  mixins: [echoMixin],
  props: {
    canEdit: { type: Boolean },
    id: { type: Number },
    y: { type: Number },
    x: { type: Number },
    type: { type: String },
    container_is_input: { type: Boolean },
    container_is_output: { type: Boolean },
    destination: { type: Object },
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
    },
    selected: undefined
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
    changeDestination() {
      this.$emit('setDestination', {
        pipelineNodeId: this.id,
        destinationId: this.selected.id,
      })
    },
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
  async created() {
    if (this.container_is_output) await this.$store.dispatch('destination/fetchDestinations')
    if (this.destination) this.selected = this.destination

    if (this.selected) {
      this.$emit('setDestination', {
        pipelineNodeId: this.id,
        destinationId: this.selected?.id
      })
    }
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
