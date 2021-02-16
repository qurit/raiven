<template>
  <v-hover v-slot:default="{ hover }">
    <v-card class="pa-2" outlined flat color="primary">
      <v-row no-gutters justify="center" align="center">
        <v-col>
          <v-select v-model="match" :items="value.matchTypes" v-bind="styleAttrs"  @change="update" />
        </v-col>
        <div class="title mx-2 white--text" style="text-transform: capitalize">{{ value.table }}</div>
        <v-select
          v-if="value.type.toLowerCase() === 'select'"
          v-model="selected"
          v-bind="attrs"
          @change="update"
        />
        <v-combobox
          v-else-if="value.type.toLowerCase() === 'combobox'"
          v-model="selected"
          v-bind="attrs"
          @change="update"
        />
        <v-expand-x-transition>
          <v-icon-btn v-if="hover" delete color="accent" @click="$emit('delete')"/>
        </v-expand-x-transition>
      </v-row>
    </v-card>
  </v-hover>
</template>

<script>
import {toPropFormat} from "@/utilities/propHelpers";

export default {
  name: 'ConditionRule',
  props: {
    value: null,
  },
  watch: {
    value(val) {
      if (!val) {
        this.cmp = null
        this.item = null
      } else {
        this.match = val.cmp
        this.match = val.value
      }
    }
  },
  data: () => ({
    match: null,
    item: null,
    attrs: undefined,
    selected: undefined,
    styleAttrs: {...toPropFormat(['solo', 'hide-details', 'flat', 'return-object'])}
  }),
  created() {
    this.attrs = {
      "items": (typeof this.value.items === 'function') ? this.value.items() : this.value.items,
      "class": 'mx-2',
      "label": this.value.tag,
      "multiple": this.value.multiple,
      "chips": this.value.chips !== false,
      ...this.styleAttrs
    }

  },
  methods: {
    update() {
      this.value.match = this.match
      this.value.values = this.selected
      this.$emit('input', this.value)
    }
  }
}
</script>
<style>
#hidden-ghost .sortable-drag {
  opacity: 0;
}
</style>
