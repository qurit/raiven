<template>
  <v-card>
    <v-card-title v-text="title" />
    <v-card-text>
      <v-row>
        <v-col>
          <v-select
            :items="modalities"
            item-text="aet"
            label="from"
            solo
            flat
            dense
            single-line
          />
        </v-col>
        <v-col>
          <v-select
            :items="modalities"
            item-text="aet"
            label="to"
            solo
            flat
            dense
            single-line
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-combobox
            :items="descriptions"
            label="Series Descriptions"
            solo
            flat
            dense
            single-line
            multiple
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-file-input solo @change="parse"/>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="6">
          <v-data-table :items="data" :headers="headers"/>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: "MoveForm",
  data: () => ({
    title: 'Query and Move',
    file: undefined,
    descriptions: ["CT WB 50cm", "PET HD AC", "PET TOF AC"],
    headers: undefined,
    data: undefined
  }),
  computed: {
    ...mapState('modalities', ['modalities'])
  },
  created() {
    if (!this.modalities.length) this.$store.dispatch('modalities/fetchModalities')
    console.log(this)
  },
  methods: {
    parse(file) {
      this.$papa.parse(file, {
        header: true,
        complete: results => {
          this.data = results.data
          this.headers = results.meta.fields.map(x => ({ text: x, value: x}))
        }
      })
    }
  }
}
</script>
