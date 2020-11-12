<template>
  <v-row>
    {{ $auth.user }}
    <v-btn @click="$auth.logout('local')">Logout</v-btn>
    <v-row justify="center">
      <UserGuide />
    </v-row>
  </v-row>
</template>

<script>
import UserGuide from '../components/UserGuide'
export default {
  components: { UserGuide }
}
</script>
