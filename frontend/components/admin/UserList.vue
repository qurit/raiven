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
      <template v-slot:item.ae_title="{ item }">
        <v-edit-dialog
          :return-value.sync="item.ae_title"
          @save="saveAETitle(item)"
        >
          {{ item.ae_title }}
          <template v-slot:input>
            <v-text-field
              v-model="item.ae_title"
              label="Edit"
              single-line
              :rules="[
                rules.validateLength,
                rules.validateASCII,
                rules.validateUserPrefix
              ]"
            ></v-text-field>
          </template>
        </v-edit-dialog>
      </template>
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
import { generic_get, generic_put } from '~/api'

export default {
  methods: {
    formatDateTime(datetime) {
      return datetime ? new Date(datetime).toLocaleString() : 'Invalid Date'
    },
    async saveAETitle(user) {
      const { ae_title } = user
      if (
        this.rules.validateLength(ae_title) === true &&
        this.rules.validateASCII(ae_title) === true &&
        this.rules.validateUserPrefix(ae_title) === true
      ) {
        const URL = `/user/${user.id}/update-ae-title`
        const payload = {
          ae_title: ae_title
        }
        await generic_put(this, URL, payload)
        this.$toaster.toastSuccess('AE Title updated!')
      } else {
        this.$toaster.toastError(
          'Could not save, make sure you have properly formed the AE title'
        )
      }
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
      sortDesc: false,
      rules: {
        validateLength(value) {
          return (
            value.trim().length <= 12 ||
            'AE Title is too long, 12 characters max'
          )
        },
        validateASCII(value) {
          if (!!value) {
            return /^[\x00-\x7F]*$/.test(value) || 'ASCII Characters only'
          }
        },
        validateUserPrefix(value) {
          return (
            value.substring(0, 4) === 'RVU-' ||
            "User AE Titles should have an 'RVU-' prefix"
          )
        }
      }
    }
  },
  created() {
    this.getUsers()
  }
}
</script>
