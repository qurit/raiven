<!--suppress ES6ModulesDependencies -->
<template>
  <v-card>
    <v-card-title>Docker Containers<v-icon right >mdi-docker</v-icon></v-card-title>
    <v-data-table
      :items="containers"
      :headers="headers"
    >
      <template
        v-slot:item.State.StartedAt="{ item }"
      >
        {{ new Date(item.State.StartedAt).toLocaleString() }}
      </template>
    </v-data-table>
    <v-card-text>
      Worker Containers: {{ workers.length }}
      <v-icon-btn @click="scaleWorkers(workers.length - 1)" minus />
      <v-icon-btn @click="scaleWorkers(workers.length + 1)" plus />
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: "DockerList",
  data: () => ({
    headers: [
      { text: 'Name', value: 'Name' },
      { text: 'Status', value: 'State.Status' },
      { text: 'Started At', value: 'State.StartedAt' },
    ]
  }),
  computed: {
    ...mapState('containers', ['containers']),
    ...mapGetters('containers', ['workers']),

  },
  created() {
    this.$store.dispatch('containers/fetchContainers')
  },
  methods: {
    ...mapActions('containers', ['scaleWorkers']),
  }
}
</script>
