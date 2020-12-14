<template>
  <v-navigation-drawer class="pt-3" app right style="z-index: 9999">
    <template v-slot:prepend>
      <v-row no-gutters justify="center" class="px-2">
        <v-btn
          @click="$emit('open-container-form')"
          color="primary accent--text"
          style="width: available"
          class="mx-auto"
          rounded
          block
        >
          Add a Container
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-row>
      <v-row no-gutters class="pt-2 px-2">
        <v-text-field
          v-model="search"
          placeholder="Search container"
          append-icon="mdi-magnify"
          solo
          flat
          rounded
          block
          color="primary"
          single-line
          hide-details
        />
      </v-row>
    </template>
    <ContainerCard
      v-for="c in filteredList"
      :id="c.id"
      :container="c"
      :colors="colors.container"
      class="ma-2"
    >
      <v-icon-btn add @click="$emit('add-node', c)" color="white" />
    </ContainerCard>
  </v-navigation-drawer>
</template>

<script>
import ContainerCard from '~/components/flowchart/ContainerCard'

export default {
  components: {
    ContainerCard
  },
  props: {
    containers: Array,
    colors: Array
  },
  data() {
    return {
      search: '',
      containerList: false
    }
  },
  computed: {
    filteredList() {
      return this.containers.filter(container =>
        container.name.toLowerCase().includes(this.search.toLowerCase())
      )
    }
  }
}
</script>
