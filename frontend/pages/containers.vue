<template>
  <div>
    <v-row>
      <v-col sm="12" md="5">
        <ContainerForm />
      </v-col>
      <v-col sm="12" md="5">
        <ContainerList />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import ContainerList from '~/components/container/ContainerList'
import ContainerForm from '~/components/container/ContainerForm'
export default {
  components: { ContainerList, ContainerForm }
}
</script>
