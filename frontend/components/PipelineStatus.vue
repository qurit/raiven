<template>
<v-card elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title> <b>Pipelines in Progress</b></v-toolbar-title>
    </v-toolbar>
    <v-divider light />
    <div v-if="pipelines.length > 0">
      <!-- comment out for now because need to figure out how to do it properly with websockets and stuff -->
      <!-- <v-flex v-for="pipeline in pipelines" :key="pipeline.id">
        <v-card>
          <v-card-subtitle>
            {{ pipeline.title }}
          </v-card-subtitle>
          <v-flex>
            <v-progress-linear
              color="light-blue"
              buffer-value="0"
              :value="pipeline.status"
              stream
            ></v-progress-linear>

            <v-btn color="error" class="ma-2">
              Stop
            </v-btn>
          </v-flex>
        </v-card>
      </v-flex> -->
    </div>
    <div v-else>
      <v-card>
      <v-card-title>
        You have no pipelines running.
      </v-card-title>
      <v-btn class="ma-2">
          <nuxt-link to="/pipeline">
            View Pipelines
          </nuxt-link>
      </v-btn>
      </v-card>
    </div>
  </div>
  </v-card>
</template>

<script>
export default {
  name: 'PipelineStatus',
  props: ['pipelines']
}
</script>
