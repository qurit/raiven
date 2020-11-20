<template>
  <v-card elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Your Containers</b></v-toolbar-title>
      <v-spacer />
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        hide-details
        solo
      />
    </v-toolbar>
    <v-divider light />
    <v-data-table
      :items="users"
      :headers="headers"
      :search="search"
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
    >
      <template v-slot:item.is_admin="{ item }">
        <v-simple-checkbox :value="item.is_admin" disabled />
      </template>
      <template v-slot:item.first_seen="{ item }">
        {{ formatDateTime(item.first_seen) }}
      </template>
      <template v-slot:item.last_seen="{ item }">
        {{ formatDateTime(item.last_seen) }}
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import { generic_get } from '~/api'

export default {
  methods: {
    formatDateTime(datetime) {
      return datetime ? new Date(datetime).toLocaleString() : 'Invalid Date'
    },
    async getUsers() {
      const URL = '/user'
      this.users = await generic_get(this, URL)
    }
  },
  data() {
    return {
      search: '',
      users: [],
      headers: [
        { text: 'Name', value: 'name' },
        { text: 'Username', value: 'username' },
        { text: 'Admin', value: 'is_admin' },
        { text: 'AE Title', value: 'ae_title' },
        { text: 'First Seen', value: 'first_seen' },
        { text: 'Last Seen', value: 'last_seen' }
      ],
      sortBy: 'name',
      sortDesc: false
    }
  },
  created() {
    this.getUsers()
  }
}
</script>
