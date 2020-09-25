<template>
  <v-row justify="center" align="center" style="height: inherit">
    <v-col cols="12">
      <div class="display-3 text-center">CRC Imaging Pipeline</div>
      <div class="mx-auto mt-8" style="max-width: 500px">
        <v-text-field
          v-model="username"
          :error="error"
          label="Username"
          prepend-inner-icon="mdi-account"
          type="text"
          solo
          flat
        />
        <v-text-field
          v-model="password"
          @keypress.enter="login"
          :error="error"
          label="Password"
          prepend-inner-icon="mdi-lock"
          type="password"
          solo
          flat
        />
        <v-row no-gutters>
          <v-spacer />
          <v-btn @click="login" rounded color="primary" light class="px-4">
            <v-icon v-text="'mdi-lock'" />
            Login
          </v-btn>
        </v-row>
      </div>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'login',
  layout: 'fullHeight',
  data: () => ({
    username: '',
    password: ''
  }),
  methods: {
    login() {
      this.$axios.post('/')
    }
  }
}
</script>
