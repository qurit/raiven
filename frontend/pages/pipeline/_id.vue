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
          icon="mdi-keyboard-return"
          color="#373740"
          to="/pipeline"
        />
           <v-icon-btn
          color="#373740"
          @click="
            pipelineDialog = true
            containerList = false"
          icon="mdi-information"
        />
        </v-icon-btn>
        <div v-if="canEdit">
          <v-icon-btn
            save
            color="#373740"
            @click="savePipeline"

          />
          <v-icon-btn
          color="#373740"
          @click="containerList = !containerList"
          :icon="
            containerList ? 'mdi-arrow-collapse-right' : 'mdi-arrow-expand-left'
          "
        />
        </div>
        <div v-if="h">
          No containers!
        </div>
      </v-row>

      <!-- Pipeline Builder -->
      <SimpleFlowchart
        :scene.sync="scene"
        :id="pipeline_id"
        :colors="colors.container"
        :canEdit="canEdit"
        ref="simpleFlowchart"
      >
        <!-- This overlay is shown if the pipeline is empty and it is the shared user viewing it -->
        <v-overlay v-if="!isFetching && !canEdit && !scene.nodes.length" absolute color="primary" class="display-3 accent--text" opacity="100">
          <v-row no-gutters justify="center">
              This Pipeline has no nodes yet.
          </v-row>
          <v-row no-gutters justify="center" class="pt-8">
            <v-btn class="mx-auto" to="/pipeline" text outline color="accent" rounded>
              <v-icon>mdi-arrow-left</v-icon>
             Take me back
            </v-btn>
          </v-row>
        </v-overlay>
      </SimpleFlowchart>

      <!-- Dialogs -->

      <v-dialog v-model="containerDialog" max-width="900px" min-height="600px">
        <ContainerForm
          :isEditing="false"
          @closeDialog="containerDialog = false"
        />
      </v-dialog>
      <v-dialog v-model="pipelineDialog" max-width="1150px" min-height="600px">
        <PipelineInfo :pipelineId="this.pipeline_id" />
      </v-dialog>

      <!-- Container List -->
      <v-navigation-drawer
        v-model="containerList"
        class="pt-3"
        app
        right
        style="z-index: 9999"
      >
        <template v-slot:prepend>
          <v-row no-gutters justify="center" class="px-2">
            <v-btn
              @click="containerDialog = true"
              color="primary accent--text"
              style="width: available"
              class="mx-auto"
              rounded
              block
            >
              Add a Container
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-row>
          <v-row no-gutters class="pt-2 px-2">
            <v-text-field
              v-model="search"
              placeholder="Search container"
              append-icon="mdi-magnify"
              solo
              flat
              rounded
              block
              color="primary"
              single-line
              hide-details
            />
          </v-row>
        </template>
        <ContainerCard
          v-for="c in filteredList"
          :id="c.id"
          :container="c"
          :colors="colors.container"
          class="ma-2"
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
import PipelineInfo from '~/components/PipelineInfo'
import { ContainerForm, ContainerCard } from '~/components/container'
import { OutputDestinationForm } from '~/components/pipeline'
import VIconBtn from '~/components/global/v-icon-btn'


export default {
  components: {
    ContainerCard,
    VIconBtn,
    SimpleFlowchart,
    ContainerForm,
    PipelineInfo
  },
  data: () => ({
    isFetching: true,
    search: '',
    userId: '',
    containerList: false,
    containerDialog: false,
    pipelineDialog: false,
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
    addNode(container) {
      let maxID = Math.max(0, ...this.scene.nodes.map(link => link.id))
      this.scene.nodes.push({
        id: maxID + 1,
        x: -400,
        y: 50,
        type: container.name,
        container_id: container.id,
        container_is_input: container.is_input_container,
        container_is_output: container.is_output_container
      })
    },
    savePipeline() {
      this.$refs.simpleFlowchart.savePipeline()
      this.containerList = false
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
      this.isFetching = false
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
      const URL = `pipeline/${this.pipeline_id}`
      try {
        const { nodes, links, user_id } = await generic_get(this, URL)
        this.getPipelineNodes(nodes)
        this.getPipelineLinks(links)
        this.userId = user_id
        if (this.canEdit) {
          this.containerList = true
        }
      } catch (e) {
        console.log(e)
      }
    }
  },
  computed: {
    ...mapState('containers', ['containers']),
    filteredList() {
      return this.containers.filter(container =>
        container.name.toLowerCase().includes(this.search.toLowerCase())
      )
    },
    canEdit() {
      return this.userId === this.$auth.user.id
    }
  },
  created() {
    this.pipeline_id = parseInt(this.$router.history.current.params.id)
    this.getContainers()
    this.getSavedPipeline(this.pipeline_id)
  }
}
</script>
