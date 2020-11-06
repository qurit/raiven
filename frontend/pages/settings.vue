<template>
  <v-row>
    {{ $auth.user }}
    <v-btn @click="$auth.logout('local')">Logout</v-btn>

    <v-card elevation="6" width="800">
      <UserGuide />
    </v-card>
  </v-row>
</template>

<script>
import UserGuide from '../components/UserGuide'
export default {
  components: { UserGuide }
}
</script>
