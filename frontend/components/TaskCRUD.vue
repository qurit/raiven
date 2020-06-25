<template>
  <v-card>
    <v-card-title>
      Jobs
      <v-spacer />
      <v-btn
        @click="addJob"
        color="primary"
        v-text="'test'"
        text
      />
      <v-icon-btn
        @click="$store.dispatch('jobs/deleteAllJobs')"
        icon="mdi-delete"
      />
      <v-icon-btn
        @click="$store.dispatch('jobs/fetchJobs')"
        icon="mdi-refresh"
      />
    </v-card-title>
    <v-data-table
      :items="jobs"
      :headers="headers"
    />
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import VIconBtn from "./global/v-icon-btn";

export default {
  name: "TaskCRUD",
  components: {VIconBtn},
  data: () => ({
    headers: [
      { text: 'Job Id', value: 'pid' },
      { text: 'Job', value: 'info' },
      { text: 'Status', value: 'status' },
    ]
  }),
  computed: {
    ...mapState('jobs', ['jobs'])
  },
  created() {
    this.$store.dispatch('jobs/fetchJobs')
  },
  methods: {
    addJob() {
      this.$store.dispatch('jobs/addJob')
    }
  }
}
</script>
