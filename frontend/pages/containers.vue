<template>
  <div>
    <v-row align="center" justify="center">
      <v-col sm="12" md="12">
        <ContainerList />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { ContainerList } from '~/components/container'

export default {
  components: { ContainerList }
}
</script>
