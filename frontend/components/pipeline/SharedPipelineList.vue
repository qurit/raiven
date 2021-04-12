<template>
  <v-card
    elevation="6"
    max-height="750"
    class="overflow-y-auto overflow-x-hidden"
    :class="'dark'"
  >
    <v-card-header title="Shared Pipelines" v-model="search" searchable />
    <v-data-table
      id="Pipelines"
      :headers="headers"
      :items="items"
      :search="search"
      class="row-pointer"
      @click:row="viewPipeline"
    />
  </v-card>
</template>

<script>
export default {
  name: 'SharedPipelineList',
  data() {
    return {
      search: '',
      headers: [
        { text: 'Pipeline Name', value: 'name' },
        { text: 'AE Title', value: 'ae_title' }
      ]
    }
  },
  computed: {
    items() {
      return this.$store.getters['pipelines/sharedPipelines']
    }
  },
  created() {
    this.$store.dispatch('pipelines/fetchPipelines')
  },
  methods: {
    viewPipeline(pipeline) {
      this.$router.push({ path: `/pipeline/${pipeline.id}` })
    }
  }
}
</script>

<style lang="css" scoped>
.row-pointer >>> tbody tr :hover {
  cursor: pointer;
}
</style>
