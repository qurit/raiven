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
    <v-divider class="my-3" light />
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
      @change="didChangeAE = true"
    >
    </v-select>
    <v-row justify="center" align="center">
      Add A Destination
      <v-icon-btn add @click="destinationDialog = true" />
    </v-row>
    <v-divider class="my-3" light />
    <v-card-actions class="justify-center">
      <v-btn
        @click="submit"
        text
        color="confirm"
        :disabled="!(didEdit && isFormValid)"
        >Save Changes</v-btn
      >
    </v-card-actions>
    <v-dialog v-model="destinationDialog" max-width="900px" min-height="600px">
      <OutputDestinationForm @closeDialog="destinationDialog = false" />
    </v-dialog>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import { generic_get, generic_put } from '~/api'
import { OutputDestinationForm } from '~/components/flowchart'
export default {
  components: {
    OutputDestinationForm
  },
  data() {
    return {
      destinationDialog: false,
      isFormValid: false,
      didChangeAE: false,
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
      return this.currentAETitle !== this.aeTitle || this.didChangeAE
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
      await generic_put(this, URL, payload)
    },
    async submit() {
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
