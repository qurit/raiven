<template>
  <div>
    <v-row>
      <v-col sm="12" md="5">
        <UserSettings />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { UserSettings } from '~/components/user'

export default {
  components: { UserSettings }
}
</script>
