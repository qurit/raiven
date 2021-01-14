<template>
  <v-app>

    <v-main id="splash">
      <v-container fill-height>
        <nuxt />
      </v-container>
    </v-main>



  </v-app>
</template>

<style>
  #splash {
    background-image: url("../assets/home.svg");

    /*background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)) , url("../static/raven.jpg") center center;*/
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
  }
</style>
