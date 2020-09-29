<template>
  <v-card>
    *** FULFILLS: As a researcher, I would like to be able to add too add to the
    list of components. ***
    <v-card-title>
      Your Containers
    </v-card-title>
    <!-- {{ console.log(containers) }} -->
    <!-- <v-list color="purple" /> -->
    <v-card-text>
      <v-list v-for="container in containers" :key="container.id">
        {{ container.title }}
        <v-btn x-small color="blue" @click="deleteContainer(container)">
          Delete
        </v-btn>
      </v-list>
    </v-card-text>
    <v-file-input label="Upload new container" @change="selectFile" />

    <!-- Jobs
      <v-spacer />
      <v-btn @click="addJob" color="primary" v-text="'test'" text />
      <v-icon-btn @click="$store.dispatch('jobs/deleteAllJobs')" delete />
      <v-icon-btn @click="$store.dispatch('jobs/fetchJobs')" refresh /> -->

    <!-- <v-data-table :items="jobs" :headers="headers" /> -->
  </v-card>
</template>

<script>
import { containers } from 'vuex'

export default {
  data: function() {
    return {
      containers: this.$store.state.containers.containers,
      currentFile: ''
    }
  },
  // computed: {
  //   getContainers() {
  //     return this.$store.state.containers.containers
  //   }
  // },
  methods: {
    selectFile(file) {
      if (file) {
        this.currentFile = file
        console.log(file)
        this.$store.commit('containers/add', { id: 4, title: file.name })
      }
    },
    deleteContainer(container) {
      this.$store.commit('containers/delete', container)
    }
  }
}
</script>
