<template>
  <v-card elevation="6" class="overflow-x-hidden">
    <v-card-title class="justify-center">
      Logout?
    </v-card-title>
    <v-card-actions class="justify-center">
      <v-btn color="confirm" class="ma-4" text @click="$auth.logout('local')">
        Yes
      </v-btn>
      <v-btn color="cancel" class="ma-4" text @click="$emit('cancel')">
        No
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
