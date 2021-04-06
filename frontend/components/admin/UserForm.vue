<template>
  <v-card class="overflow-x-hidden overflow-y-hidden">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title v-text="title" class="font-weight-bold" color="accent" />
      <v-spacer />
    </v-toolbar>
    <v-form v-model="isFormValid" ref="form">
      <v-text-field
        v-model="name"
        label="Name"
        required
        :rules="[validateNotEmpty]"
        class="px-15 pt-5"
      />
      <v-text-field
        v-model="username"
        label="Username"
        required
        :rules="[validateNotEmpty]"
        class="px-15 pt-5"
      />
      <v-text-field
        v-model="password"
        label="Password"
        :append-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append="() => (visible = !visible)"
        :type="visible ? 'text' : 'password'"
        :rules="[validateNotEmpty]"
        required
        class="px-15 pt-5"
      />
      <v-text-field
        v-model="passwordConfirm"
        label="Confirm Password"
        :append-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append="() => (visible = !visible)"
        :type="visible ? 'text' : 'password'"
        :rules="
          [validateNotEmpty] &&
            (this.password === this.passwordConfirm || ['Passwords must match'])
        "
        required
        class="px-15 pt-5"
      />
    </v-form>
    <v-row justify="center" align="center">
      <v-icon-btn
        save
        :disabled="!isFormValid"
        @click="saveUser"
        color="confirm"
        class="ma-4"
      />
    </v-row>
  </v-card>
</template>

<script>
import { validateNotEmpty } from '~/utilities/validationRules'

export default {
  data: () => ({
    title: 'Add A User',
    visible: false,
    isFormValid: false,
    name: '',
    username: '',
    password: '',
    passwordConfirm: ''
  }),
  computed: {
    samePassword() {
      return password === passwordConfirm
    }
  },
  methods: {
    validateNotEmpty,
    async saveUser() {
      const payload = {
        name: this.name,
        username: this.username,
        password: this.password
      }
      await this.$store.dispatch('users/addUser', payload)
      this.$refs.form.reset()
      this.visible = false
      this.$emit('closeAddUserForm')
    }
  }
}
</script>
