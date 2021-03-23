<template>
  <div>
    <v-row>
      <v-col sm="12" md="9">
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
