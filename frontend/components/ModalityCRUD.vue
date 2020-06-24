<template>
  <v-card :loading="isLoading" >

    <!-- Header -->
    <v-card-title>
      {{ title }}
      <v-spacer />
      <v-expand-x-transition>
        <v-icon-btn v-if="showForm" @click="saveModality" icon="mdi-content-save" />
      </v-expand-x-transition>
      <v-fade-transition>
        <v-icon-btn v-if="showForm" @click="showForm = false" icon="mdi-minus" />
        <v-icon-btn v-if="!showForm" @click="showForm = true" />
      </v-fade-transition>
    </v-card-title>

    <!-- Modalities -->
    <v-divider v-if="modalities.length"/>
    <v-list v-if="modalities.length" dense flat>
      <v-list-item-group v-model="selected">
         <v-list-item v-for="(m, i) in modalities" :key="i" :ripple="false">
          <v-row no-gutters>
            {{ m.aet }} {{ `${m.address} - ${m.port}`}}
            <v-spacer />
            <v-icon-btn icon="mdi-wifi-strength-4" @click.stop.native="echo(m)" />
            <v-expand-x-transition v-if="selected === i">
              <v-icon-btn icon="mdi-delete" color="tertiary" @click="deleteModality(m)" />
            </v-expand-x-transition>
          </v-row>
        </v-list-item>
      </v-list-item-group>
    </v-list>

    <!-- Add Modality form -->
    <v-divider v-if="showForm" class="pb-4" />
    <v-expand-transition >
      <v-list-item v-if="showForm">
        <ModalityForm v-if="showForm" @saved="showForm = false" />
      </v-list-item>
    </v-expand-transition>

  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import { echo } from "../api/dicom";
import ModalityForm from "../components/ModalityForm";

export default {
  name: "ModalityCRUD",
  components: { ModalityForm },
  data: () => ({
    title: "Available Modalities",
    showForm: false,
    selected: undefined,
    isLoading: false
  }),
  computed: {
    ...mapState('modalities', ['modalities'])
  },
  created() {
    this.$store.dispatch('modalities/fetchModalities')
  },
  methods: {
    async echo(modality) {
      this.isLoading = true
      try {
        await echo(this, modality)
        this.$toaster.toastSuccess('Echo Succeeded')
      } catch (e) {
        this.$toaster.toastError('Echo Failed')
      } finally {
        this.isLoading = false
      }
    },
    deleteModality(modality) {
      this.$store.dispatch('modalities/deleteModality', modality)
    },
    saveModality() {
      this.$root.$emit('save-modality')
    }
  }
}
</script>
