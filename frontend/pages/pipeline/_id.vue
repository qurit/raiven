<template>
  <v-row class="pipeline-creator" no-gutters>
    <v-col cols="12">
      <v-row
        class="ma-2"
        style="position: absolute; z-index: 1;"
        no-gutters
        align="center"
      >
        <v-icon-btn
          large
          color="#373740"
          @click="savePipeline"
          icon="mdi-content-save"
        />
        <v-btn @click="containerList = !containerList" large icon>
          <v-icon
            large
            color="#373740"
            v-text="containerList ? 'mdi-minus' : 'mdi-plus'"
          />
        </v-btn>
      </v-row>

      <!-- Pipeline Builder -->
      <SimpleFlowchart
        :scene.sync="scene"
        :id="pipeline_id"
        :colors="colors.container"
        @toggle-value="toggleValue"
        ref="simpleFlowchart"
      />

      <!-- Dialogs -->
      <v-dialog v-model="containerDialog" max-width="900px" min-height="600px">
        <ContainerForm
          :isEditing="false"
          @closeDialog="containerDialog = false"
        />
      </v-dialog>

      <!-- Container List -->
      <v-navigation-drawer
        v-model="containerList"
        absolute
        right
        style="z-index: 9999"
      >
        <template v-slot:prepend>
          <v-list-item two-line>
            <v-list-item-content>
              <v-btn
                class="mt-2 mx-auto"
                @click="containerDialog = true"
                color="primary"
                outlined
                rounded
              >
                Add a Container
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-list-item-content>
          </v-list-item>
        </template>

        <ContainerCard
          v-for="c in containers"
          :id="c.id"
          :container="c"
          :colors="colors.container"
        >
          <v-icon-btn add @click="addNode(c)" color="white" />
        </ContainerCard>
      </v-navigation-drawer>
    </v-col>
  </v-row>
</template>

<script>
import { mapState } from 'vuex'
import { generic_get } from '~/api'

import SimpleFlowchart from '~/components/flowchart/SimpleFlowchart'
import VIconBtn from '../../components/global/v-icon-btn'
import ContainerForm from '~/components/container/ContainerForm'
import OutputDestinationForm from '~/components/OutputDestinationForm'
import ContainerCard from '~/components/container/ContainerCard'

export default {
  components: {
    ContainerCard,
    VIconBtn,
    SimpleFlowchart,
    ContainerForm
  },
  data: () => ({
    containerList: true,
    containerDialog: false,
    pipeline_id: '',
    colors: {
      container: {
        input: 'orange',
        output: 'purple',
        default: 'blue'
      }
    },
    scene: {
      centerX: 1024,
      centerY: 140,
      scale: 1,
      nodes: [],
      links: []
    }
  }),
  methods: {
    toggleValue(a, b, c) {
      console.log('in grandparent')
      console.log(a)
    },
    addNode(container) {
      let maxID = Math.max(0, ...this.scene.nodes.map(link => link.id))
      this.scene.nodes.push({
        id: maxID + 1,
        x: -400,
        y: 50,
        type: container.name,
        container_id: container.id,
        container_is_input: container.is_input_container,
        container_is_output: container.is_output_container,
        host: undefined,
        port: undefined
      })
    },
    savePipeline() {
      this.$refs.simpleFlowchart.savePipeline()
    },
    getContainers() {
      this.$store.dispatch('containers/fetchContainers')
    },
    getPipelineNodes(nodes) {
      nodes.forEach(node => {
        const containerNode = {
          id: node.id,
          x: node.x_coord,
          y: node.y_coord,
          container_id: node.container_id,
          type: node.container.name,
          label: node.container.description,
          container_is_input: node.container_is_input,
          container_is_output: node.container_is_output,
          destination: node.destination
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
      const URL = `pipeline/${this.pipeline_id}`
      try {
        const { nodes, links } = await generic_get(this, URL)
        console.log(nodes)
        this.getPipelineNodes(nodes)
        this.getPipelineLinks(links)
      } catch (e) {
        console.log(e)
      }
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
