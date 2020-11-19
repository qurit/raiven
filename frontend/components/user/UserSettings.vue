<template>
  <v-card elevation="6">
    <v-toolbar color="primary accent--text" flat>
      <v-toolbar-title><b>Settings</b></v-toolbar-title>
    </v-toolbar>
    <v-form v-model="isFormValid">
      <v-text-field
        class="mx-2"
        v-model="aeTitle"
        :rules="[rules.validateLength, rules.validateASCII]"
        counter
        prefix="Your AE Title is: RVU-"
        prepend-icon="mdi-access-point"
      ></v-text-field>
    </v-form>
    <v-card-actions class="justify-center">
      <v-btn
        @click="submit"
        text
        color="confirm"
        :disabled="!(didEdit && isFormValid)"
        >Save Changes</v-btn
      >
    </v-card-actions>
  </v-card>
</template>

<script>
import { generic_get, generic_put } from '~/api'
export default {
  data() {
    return {
      isFormValid: false,
      aeTitle: '',
      currentAETitle: '',
      rules: {
        validateLength(value) {
          return (
            value.trim().length <= 12 ||
            'AE Title is too long, 12 characters max'
          )
        },
        validateASCII(value) {
          if (!!value) {
            return /^[\x00-\x7F]*$/.test(value) || 'ASCII Characters only'
          }
        }
      }
    }
  },
  computed: {
    didEdit() {
      return this.currentAETitle !== this.aeTitle
    }
  },
  methods: {
    async submit() {
      try {
        const URL = '/user/edit'
        const payload = {
          ae_title: this.aeTitle
        }
        const newAETitle = await generic_put(this, URL, payload)
        this.ae_title = newAETitle
        this.$toaster.toastSuccess('Changes saved!')
      } catch (e) {
        this.$toaster.toastError('Could not save changes')
      }
    },
    async getUserInfo() {
      const URL = '/user/me'
      const { ae_title } = await generic_get(this, URL)
      this.aeTitle = ae_title
      this.currentAETitle = ae_title
    }
  },
  created() {
    this.getUserInfo()
  }
}
</script>
