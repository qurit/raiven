<template>
  <v-card elevation="6" v-if="this.$auth.user.is_admin" flat>
    <v-card-header title="LDAP Users" v-model="search" searchable />
    <v-data-table
      :items="users"
      :headers="headers"
      :search="search"
      sort-by="title"
    />
  </v-card>
</template>

<script>
import { generic_get } from '~/api'

export default {
  name: 'UserLDAP',
  data: () => ({
    search: '',
    headers: [
      { text: 'Title', value: 'title' },
      { text: 'Department', value: 'department' },
      { text: 'Company', value: 'company' }
    ],
    users: []
  }),
  created() {
    this.getUsers()
  },
  methods: {
    async getUsers() {
      const URL = 'user/ldap'
      this.users = await generic_get(this, URL)
    }
  }
}
</script>
