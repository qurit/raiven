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
    <v-select
      multiple
      class="mx-2"
      hint="Choose which Association Entities can send to you"
      persistent-hint
      :items="destinations"
      item-text="full_name"
      return-object
      label="Allowed Association Entities"
      v-model="permittedAETitles"
      chips
      clearable
    >
    </v-select>
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
import { mapState } from 'vuex'
import { generic_get, generic_put } from '~/api'
export default {
  data() {
    return {
      isFormValid: false,
      associationEntities: [],
      permittedAETitles: [],
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
    ...mapState('destination', ['destinations']),
    didEdit() {
      return this.currentAETitle !== this.aeTitle
    }
  },
  methods: {
    async getUserInfo() {
      const URL = '/user/me'
      const { ae_title } = await generic_get(this, URL)
      this.aeTitle = ae_title
      this.currentAETitle = ae_title
    },
    async getUserDestinations() {
      const URL = '/destination/user-destination'
      const userPermittedDestinations = await generic_get(this, URL)
      userPermittedDestinations.forEach(permitted => {
        this.permittedAETitles.push(permitted.destination)
      })
      console.log(this.permittedAETitles)
    },
    async saveUserAETitle() {
      const URL = '/user/edit'
      const payload = {
        ae_title: this.aeTitle
      }
      const newAETitle = await generic_put(this, URL, payload)
      this.ae_title = newAETitle
    },
    async savePermittedAETitles() {
      const URL = '/destination/user-destination'
      const payload = {
        destinations: this.permittedAETitles
      }
      console.log(payload)
      await generic_put(this, URL, payload)
    },
    async submit() {
      console.log(this.destinations)
      try {
        await this.saveUserAETitle()
        await this.savePermittedAETitles()
        this.$toaster.toastSuccess('Changes saved!')
      } catch (e) {
        this.$toaster.toastError('Could not save changes')
      }
    }
  },
  created() {
    this.$store.dispatch('destination/fetchDestinations')
    this.getUserInfo()
    this.getUserDestinations()
  }
}
</script>
