<template>
  <v-card flat width="700" v-if="node">
    <v-toolbar flat tile color="primary accent--text" dense>
      Condition Builder
      <v-spacer />
      <v-select
        :items="rules"
        v-model="selectedRule"
        item-text="tag"
        return-object
        dense
        solo
        single-line
        hide-details
        flat
        style="max-width: 200px"
      />
      <v-icon-btn
        plus
        @click="addRule(selectedRule)"
        :disabled="!selectedRule"
        icon
        dark
        class="ml-2"
        color="accent"
      />
    </v-toolbar>
    <v-system-bar lights-out>
      Setting Rules for {{ node.type
      }}{{
        node.destination ? ' going to ' + node.destination.title : ''
      }}</v-system-bar
    >
    <v-card-text>
      <v-list-item :key="i" v-for="(rule, i) in query" no-gutters class="py-1">
        <ConditionRule
          v-model="query[i]"
          :items="rule.items"
          :comparators="rule.comparators"
          :key="rule.id"
          @delete="deleteRule(i)"
          @input="updateRule(i)"
        />
      </v-list-item>
    </v-card-text>
    <v-card-actions>
      <slot name="actions" />
    </v-card-actions>
  </v-card>
</template>

<script>
import VIconBtn from '../global/v-icon-btn.vue'
import ConditionRule from './ConditionRule'
import { rules } from './rules'
export default {
  name: 'ConditionBuilder',
  components: { ConditionRule, VIconBtn },
  props: {
    node: {
      type: Object,
      default: () => {}
    },
    value: {
      type: Array,
      default: () => []
    }
  },
  data: () => ({
    rules: rules,
    drag: false,
    selectedRule: undefined,
    query: [],
    sub: undefined
  }),
  mounted() {
    if (this.rules) this.selectedRule = this.rules[0]
    if (this.node && this.node.conditions)
      this.node.conditions.forEach(condition => {
        const rule = this.rules.find(r => r.tag === condition.tag)
        this.addRule(rule, condition)
      })
  },
  methods: {
    addRule(r, v = undefined) {
      const rule = Object.assign({}, r)
      this.query.push(v ? { ...rule, values: v.values, match: v.match } : rule)
      this.value.push(v ? v : { tag: rule.tag, match: undefined, values: null })
      this.$emit('input', this.value)
    },
    updateRule(i) {
      this.value.splice(i, 1, {
        tag: this.query[i].tag,
        match: this.query[i].match,
        values: this.query[i].values
      })
      this.$emit('input', this.value)
    },
    deleteRule(i) {
      this.query.splice(i, 1)
      this.value.splice(i, 1)
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
