<template>
  <v-dialog v-model="dialog" max-width="500">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon v-text="'mdi-plus'" />
      </v-btn>
    </template>

    <v-card>
      <v-card-title v-text="title" />
      <v-card-text>
        <v-text-field solo flat type="text" label="AE Title" hint="AE Title"/>
        <v-row>
          <v-col>
            <v-text-field solo flat>sdd</v-text-field>
          </v-col>
          <v-col>
            <v-text-field solo flat>sdd</v-text-field>
          </v-col>
        </v-row>

      </v-card-text>
    </v-card>

  </v-dialog>
</template>

<script>
export default {
  name: "ModalityForm",
  data: () => ({
    dialog: true,
    title: 'Add Modality'
  })
}
</script>
