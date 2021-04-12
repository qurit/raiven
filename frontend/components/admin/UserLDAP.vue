<template>
  <v-card elevation="6" v-if="this.$auth.user.is_admin" flat>
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Users</b></v-toolbar-title>
      <v-spacer />
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        hide-details
        solo
      />
      <v-icon-btn plus large @click="addUserForm = true" color="accent" />
    </v-toolbar>
    <v-data-table
      :items="users"
      :headers="headers"
      :search="search"
      sort-by="title"
      :sort-desc="true"
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
