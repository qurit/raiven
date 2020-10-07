<template>
  <v-card>
    *** FULFILLS: As a researcher, I would like to be able to add too add to the
    list of components. ***
    <v-card-title>
      Your Containers
    </v-card-title>
    <v-btn>
      click
    </v-btn>
    <!-- {{ console.log(containers) }} -->
    <!-- <v-list color="purple" /> -->
    <v-card-text>
      <v-list v-for="container in containers" :key="container.id">
        {{ container }}
        <v-btn x-small color="blue" @click="deleteContainer(container.id)">
          Delete
        </v-btn>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  data: function() {
    return {
      currentFile: ''
    }
  },
  methods: {
    deleteContainer(containerId) {
      this.$store.dispatch('containers/deleteContainer', containerId)
    },
    click() {
      console.log(containers)
    }
  },
  computed: {
    ...mapState('containers', ['containers'])
  },
  created() {
    this.$store.dispatch('containers/fetchContainers')
  }
  // methods: {
  //   deleteContainer(container) {
  //     this.$store.commit('containers/delete', container)
  //   }
  // }
}
</script>
