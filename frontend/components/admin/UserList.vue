<template>
  <v-card elevation="6" v-if="this.$auth.user.is_admin" flat>
    <v-card-header
      title="Local Users"
      v-model="search"
      searchable
      icon="plus"
      :func="openUserForm"
    />
    <v-data-table
      :items="users"
      :headers="headers"
      :search="search"
      sort-by="name"
    >
      <template v-slot:[`item.ae_title`]="{ item }">
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
      <template v-slot:[`item.is_admin`]="{ item }">
        <v-simple-checkbox :value="item.is_admin" disabled />
      </template>
      <template v-slot:[`item.first_seen`]="{ item }">
        {{ formatDateTime(item.first_seen) }}
      </template>
      <template v-slot:[`item.last_seen`]="{ item }">
        {{ formatDateTime(item.last_seen) }}
      </template>
      <template v-slot:[`item.access_allowed`]="{ item }">
        <!-- <v-simple-checkbox
          :value="item.access_allowed"
          @click="changeAccess(item)"
          :disabled="$auth.user.id === item.id"
        /> -->

        <v-checkbox
          :input-value="item.access_allowed"
          @change="changeAccess(item)"
          :disabled="$auth.user.id === item.id"
        />
      </template>
    </v-data-table>
    <v-dialog v-model="addUserForm" max-width="900px" min-height="600px">
      <UserForm @closeAddUserForm="addUserForm = false" />
    </v-dialog>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import { validateAETitle } from '~/utilities/validationRules'
import UserForm from './UserForm'

export default {
  components: {
    UserForm
  },
  data: () => ({
    addUserForm: false,
    search: '',
    headers: [
      { text: 'Name', value: 'name' },
      { text: 'Username', value: 'username' },
      { text: 'Admin', value: 'is_admin' },
      { text: 'AE Title', value: 'ae_title' },
      { text: 'Title', value: 'ldap_user.title' },
      { text: 'Department', value: 'ldap_user.department' },
      { text: 'Company', value: 'ldap_user.company' },
      { text: 'Access', value: 'access_allowed' },
      { text: 'First Seen', value: 'first_seen' },
      { text: 'Last Seen', value: 'last_seen' }
    ]
  }),
  computed: {
    ...mapState('users', ['users']),
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
    openUserForm() {
      this.addUserForm = true
    },
    async saveAETitle({ id, ae_title }) {
      if (typeof this.validateAETitle(ae_title) === 'string')
        throw 'Validation Error'
      this.$store.dispatch('users/editUserAETitle', { id, ae_title })
    },
    changeAccess(user) {
      console.log(user)
      console.log(this.$auth.user)
      this.$store.dispatch('users/changeAccess', user.id)
    }
  }
}
</script>
