<template>
  <v-data-table
    :headers="headers"
    :items="files"
    :items-per-page="5"
    class="elevation-1"
  ></v-data-table>
</template>

<script>
import { files } from 'vuex'

export default {
  data() {
    return {
      headers: [
        {
          text: 'Store event / File name',
          align: 'start',
          sortable: false,
          value: 'name'
        },
        { text: 'Date received', value: 'date', sortable: true },
        { text: 'SCU host', value: 'host' },
        { text: 'SCU port', value: 'port' }
      ],
      files: this.$store.state.files.files
    }
  }
}
</script>
