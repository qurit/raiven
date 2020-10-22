<template>
  <v-row justify="center" align="center" style="height: inherit" no-gutters>
    <v-col cols="12">
      <div class="text-center display-4 raiven" style="font-family: 'Monoton', sans-serif !important;" v-html="title" />
      <VueTypedJs
        :typeSpeed="25"
        :showCursor="false"
        :strings="[subtitle]"
        @onComplete="complete = true">
        <div class="typing text-center title raiven"  style="width: 100%;"></div>
      </VueTypedJs>
      <v-expand-transition>
        <v-card class="mx-auto mt-8 pa-4" style="max-width: 500px; border-radius: 24px" v-if="complete">
        <v-text-field
          v-model="username"
          :error="error"
          label="Username"
          prepend-inner-icon="mdi-account"
          type="text"
          solo
          flat
          rounded
        />
        <v-text-field
          v-model="password"
          @keypress.enter="login"
          :error="error"
          label="Password"
          prepend-inner-icon="mdi-lock"
          type="password"
          flat
          solo
          rounded
        />
        <v-row no-gutters>
          <v-spacer />
          <v-btn :to="'/'" @click="login" rounded color="primary secondary--text" light class="px-4">
            <v-icon v-text="'mdi-lock'" />
            Login
          </v-btn>
        </v-row>
      </v-card>
      </v-expand-transition>
    </v-col>

<!-- qurit logo   -->
    <v-img src="qurit-logo.png" max-width="150px" contain id="qurit" class="pa-4" />
  </v-row>
</template>

<script>
import { VueTypedJs } from 'vue-typed-js'
export default {
  name: 'login',
  layout: 'fullHeight',
  components: {VueTypedJs},
  data: () => ({
    username: '',
    password: '',
    complete: false,
    title: 'R<span>AI</span>VEN',
    subtitle: 'The <span>AI</span> Radiology Environment of the Future'

  }),
  methods: {
    login() {
      this.$axios.post('/')
    }
  }
}
</script>
<style lang="scss">
  .title,
  .display-4 {
    color: #33333d;
  }

  .raiven > span {
    color: var(--v-primary-base)
  }

  .display-4 {
    transition: color 5s linear;
  }

  #qurit {
    position:fixed;
    bottom:0;
  }
</style>
