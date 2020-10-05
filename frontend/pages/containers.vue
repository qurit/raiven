<template>
  <div>
    <v-row>
      <v-col cols="6">
        <ContainerForm />
      </v-col>
      <v-col cols="6">
        <ContainerList />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import ContainerList from '../components/ContainerList'
import ContainerForm from '../components/ContainerForm'
export default {
  components: { ContainerList, ContainerForm }
}
</script>
