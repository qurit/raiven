<template>
  <div>
    <v-row>
      <v-col cols="12">
        <UserList />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { UserList } from '~/components/admin'
export default {
  middleware: 'admin',
  components: { UserList }
}
</script>
