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
          placeholder="Search by name or tag"
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
      :key="c.id"
      :id="c.id"
      :container="c"
      :colors="colors.container"
      class="ma-2"
    >
      <v-spacer />
      <v-icon-btn @click="$emit('add-node', c)" color="white" />
    </ContainerCard>
  </v-navigation-drawer>
</template>

<script>
import ContainerCard from './ContainerCard'

export default {
  name: 'ContainerDrawer',
  components: { ContainerCard },
  props: {
    containers: Array,
    colors: Object
  },
  data: () => ({
    search: '',
    containerList: false
  }),
  computed: {
    filteredContainerName: ctx =>
      ctx.containers.filter(c =>
        c.name.toLowerCase().includes(ctx.search.toLowerCase())
      ),
    filteredContainerTags: ctx =>
      ctx.containers.filter(c =>
        c.tags
          .map(tag => tag.tag_name.toLowerCase().trim())
          .join()
          .includes(ctx.search.toLowerCase())
      ),
    filteredContainerAuthor: ctx =>
      ctx.containers.filter(c =>
        c.user.name.toLowerCase().includes(ctx.search.toLowerCase())
      ),
    filteredList: ctx => [
      ...new Set([
        ...ctx.filteredContainerName,
        ...ctx.filteredContainerTags,
        ...ctx.filteredContainerAuthor
      ])
    ]
  }
}
</script>

<style>
.v-text-field ::placeholder {
  font-size: 0.9em;
}
</style>
