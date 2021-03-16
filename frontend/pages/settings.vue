<template>
  <div>
    <v-row>
      <v-col sm="12" md="5">
        <UserSettings />
      </v-col>
      <v-col sm="12" md="7">
        <Conditions />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { UserSettings, Conditions } from '~/components/user'

export default {
  components: { UserSettings, Conditions }
}
</script>
