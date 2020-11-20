<template>
  <v-card elevation="6">
    <v-data-table :items="users" :headers="headers">
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
      users: [],
      headers: [
        { text: 'Name', value: 'name' },
        { text: 'Username', value: 'username' },
        { text: 'Admin', value: 'is_admin' },
        { text: 'AE Title', value: 'ae_title' },
        { text: 'First Seen', value: 'first_seen' },
        { text: 'Last Seen', value: 'last_seen' }
      ]
    }
  },
  created() {
    this.getUsers()
  }
}
</script>
