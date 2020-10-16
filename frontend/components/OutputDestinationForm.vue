<template>
  <v-card class="overflow-x-hidden">
    <v-form v-model="form" class="ma-5">
      <v-card-title> Add a destination source for your pipelines </v-card-title>
      <v-row>
        <v-col cols="6">
          <v-text-field
            v-model="hostAddressName"
            label="Host Address"
            :rules="[v => !!v || 'A Host Address is required']"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="portName"
            label="Port"
            :rules="[v => !!v || 'A Port is required']"
            required
          ></v-text-field>
        </v-col>
      </v-row>
    </v-form>
    <v-row justify="center">
      <v-btn class="ma-4" color="green">
        Add
      </v-btn>
    </v-row>
  </v-card>
</template>
