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
      currentFile: '',
      containers: ''
    }
  },
  methods: {
    getContainers() {
      const path = 'http://localhost:5000/container'
      axios
        .get(path)
        .then(res => {
          this.containers = res.data
        })
        .catch(err => {
          console.log(err)
          this.getContainers()
        })
    },
    deleteContainer(containerId) {
      const path = `http://localhost:5000/container/${containerId}`
      axios
        .delete(path)
        .then(res => {
          this.getContainers()
        })
        .catch(err => {
          console.log(err)
          this.getContainers()
        })
    }
  },
  created() {
    this.getContainers()
  }
  // computed: {
  //   ...mapState('containers', ['containers'])
  // },
  // methods: {
  //   deleteContainer(container) {
  //     this.$store.commit('containers/delete', container)
  //   }
  // }
}
</script>
