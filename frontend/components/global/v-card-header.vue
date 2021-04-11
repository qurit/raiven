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
      label="Search by
    Name or File"
      hide-details
      @input="$emit('input', $event)"
      solo
    />
    <v-icon-btn @click="func" color="#373740" :icon="icon" />
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
      type: String
    },
    searchable: {
      type: Boolean,
      default: false
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
