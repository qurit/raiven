<template>
  <div>
    <v-row>
      <v-col sm="12" md="5">
        <ContainerForm />
      </v-col>
      <v-col sm="12" md="7">
        <ContainerList />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { ContainerForm, ContainerList } from '~/components/container'

export default {
  components: { ContainerList, ContainerForm }
}
</script>
