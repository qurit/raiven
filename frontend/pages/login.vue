<template>
  <v-row justify="center">
    <div class="h1">sddsadssd</div>
    <v-card dark min-width="500">
      <v-card-title><v-spacer />Login</v-card-title>
      <v-card-text>
         <v-text-field
            v-model="username"
            :error="error"
            label="Login"
            prepend-icon="mdi-account"
            type="text"
            color="primary"
          />
          <v-text-field
            v-model="password"
            @keypress.enter="login"
            :error="error"
            label="Password"
            prepend-icon="mdi-lock"
            type="password"
            color="primary"
          />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="login" text color="secondary">Login</v-btn>
      </v-card-actions>
    </v-card>
  </v-row>
</template>

<script>
export default {
  name: "login",
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

<style scoped>

</style>
