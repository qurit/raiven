<template>
  <v-row>
    <v-col cols="6">
      <ModalityCRUD />
    </v-col>
    <v-col cols="6">
      <DockerList />
    </v-col>
  </v-row>
</template>

<script>
import ModalityCRUD from "../components/ModalityCRUD";
import DockerList from "../components/DockerList";
export default {
  components: {DockerList, ModalityCRUD}
}
</script>
