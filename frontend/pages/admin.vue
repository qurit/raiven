<template>
  <div>
    <v-row>
      <v-col cols="12">
        <UserList />
      </v-col>
      <v-col cols="12">
        <UserLDAP />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { UserList, UserLDAP } from '~/components/admin'
export default {
  middleware: 'admin',
  components: { UserList, UserLDAP }
}
</script>
