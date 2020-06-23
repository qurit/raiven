<template>
  <v-row>
    <v-col cols="6">
      <v-card>
        <v-card-title>
          AET's
          <v-spacer />
          <ModalityForm />
        </v-card-title>
        <v-divider />
          <v-list-item v-for="m in modalities">
            <v-row no-gutters>
              {{ m.AET }}
              <v-spacer />
              <v-icon-btn icon="mdi-wifi-strength-4" @click="echo" />
              <VIconBtn />
            </v-row>
          </v-list-item>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapState } from 'vuex'
import ModalityForm from "../components/ModalityForm";
// import VIconBtn from "../components/generic/v-icon-btn";
// import VIconBtn from "../components/generic/v-icon-btn";

export default {
  name: "settings",
  components: {ModalityForm},
  computed: {
    ...mapState('modalities', ['modalities'])
  },
  created() {
    this.$store.dispatch('modalities/fetchModalities')
  },
  methods: {
    echo() {
      console.log('echo')
    }
  }
}
</script>

