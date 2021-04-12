<template>
  <v-toolbar color="primary accent--text" flat>
    <v-toolbar-title>
      <b>{{ title }} </b></v-toolbar-title
    >
    <v-spacer />
    <v-text-field
      v-model="search"
      v-if="searchable"
      append-icon="mdi-magnify"
      :label="searchLabel"
      hide-details
      @input="$emit('input', $event)"
      solo
    />
    <v-icon-btn v-if="icon" @click="func" color="accent" :icon="icon" />
  </v-toolbar>
</template>

<script>
import vIconBtn from '../global/v-icon-btn.vue'
export default {
  name: 'v-card-header',
  components: {
    vIconBtn
  },
  props: {
    title: {
      type: String
    },
    icon: {
      type: String,
      default: null
    },
    searchable: {
      type: Boolean,
      default: false
    },
    searchLabel: {
      type: String,
      default: 'Search'
    },
    func: {
      type: Function,
      default: () => undefined
    }
  },
  data: () => {
    return {
      search: ''
    }
  }
}
</script>
