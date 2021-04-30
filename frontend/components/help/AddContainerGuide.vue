<template>
  <v-card elevation="10">
    <v-card-header title="Step 2: Add a Container" />
    <v-card-subtitle>
      <b>Uploading a Container</b>
    </v-card-subtitle>
    <v-card-text>
      <ol type="1">
        <li>
          Go to the <nuxt-link to="/containers">Containers</nuxt-link>
          <v-icon small color="icon">
            mdi-package-variant-closed
          </v-icon>
          page
        </li>
        <li>
          Click <v-icon small color="icon">mdi-plus</v-icon> and fill out the
          form
        </li>
        <ul>
          <li>
            You must provide a Container name and an attached file (your zipped
            Dockerfile and main algorithm from Step 1)
          </li>
        </ul>
        <li>
          Click <v-icon small color="icon">mdi-content-save </v-icon> to save
          your Container
        </li>
      </ol>
    </v-card-text>
    <v-card-subtitle>
      <b>Editing a Container</b>
    </v-card-subtitle>
    <v-card-text>
      <ol type="1">
        <li>
          Go to the <nuxt-link to="/containers">Containers</nuxt-link>
          <v-icon small color="icon"> mdi-package-variant-closed </v-icon>
          page
        </li>
        <li>
          Click <v-icon small color="icon"> mdi-pencil </v-icon> next to the
          Container to be edited
          <ul>
            <li>
              Alternatively, click
              <v-icon small color="icon"> mdi-delete </v-icon> to completely
              delete the Container
            </li>
          </ul>
        </li>
        <li>Edit the form</li>
        <li>
          Click <v-icon small color="icon">mdi-content-save </v-icon> to save
        </li>
      </ol>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'AddContainerGuide'
}
</script>
