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
    </v-toolbar>
    <v-data-table
      :items="users"
      :headers="headers"
      :search="search"
      sort-by="name"
      :sort-desc="false"
    >
      <template v-slot:item.ae_title="{ item }">
        <v-edit-dialog :return-value="item.ae_title">
          {{ item.ae_title ? aePrefix + item.ae_title : '' }}
          <v-text-field
            slot="input"
            class="my-2"
            :value="item.ae_title"
            label="Edit"
            single-line
            hint="Press Enter to save"
            :prefix="aePrefix"
            :rules="[validateAETitle]"
            @keyup.enter="
              saveAETitle({ id: item.id, ae_title: $event.target.value })
            "
          />
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
import { mapState } from 'vuex'
import { validateAETitle } from '~/utilities/validationRules'

export default {
  data() {
    return {
      search: '',
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
  computed: {
    ...mapState('users', ['users']),
    aeTitle: {
      get() {
        return this.$store.state.user.ae_title
      },
      set(value) {
        this.$store.commit('editUserAETitle', value)
      }
    },
    aePrefix: ctx => ctx.$store.state.config.USER_AE_PREFIX
  },
  created() {
    this.$store.dispatch('users/fetchUsers')
  },
  methods: {
    validateAETitle,
    formatDateTime(datetime) {
      return datetime ? new Date(datetime).toLocaleString() : 'Invalid Date'
    },
    async saveAETitle({ id, ae_title }) {
      if (typeof this.validateAETitle(ae_title) === 'string')
        throw 'Validation Error'
      this.$store.dispatch('users/editUserAETitle', { id, ae_title })
    }
  }
}
</script>
