<template>
  <v-row>
    <v-col cols="6">
      <v-card>
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
        <v-divider />

<!-- Modalities -->
        <v-list dense flat>
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
              <ModalityForm v-if="showForm"/>
            </v-list-item>
          </v-expand-transition>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapState } from 'vuex'
import ModalityForm from "../components/ModalityForm";
import { echo } from "../api/dicom";
import VIconBtn from "../components/global/v-icon-btn";

export default {
  name: "settings",
  components: {VIconBtn, ModalityForm},
  data: () => ({
    title: "Available Modalities",
    showForm: false,
    selected: undefined
  }),
  computed: {
    ...mapState('modalities', ['modalities'])
  },
  created() {
    this.$store.dispatch('modalities/fetchModalities')
  },
  methods: {
    async echo(modality) {
      await echo(this, modality)
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

