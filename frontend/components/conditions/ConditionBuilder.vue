
<template>
  <v-card flat outlined width="1000">
    <v-sheet flat tile color="primary accent--text" >
      <v-row no-gutters align="center" class="pa-2">
        Condition Builder
        <v-spacer />
        <v-select :items="rules" v-model="selectedRule" item-text="tag" return-object dense solo single-line hide-details flat style="max-width: 200px" />
        <v-btn @click="addRule" :disabled="!selectedRule" icon dark class="ml-2">
          <v-icon v-text="'mdi-plus'" />
        </v-btn>
      </v-row>
    </v-sheet>
    <v-card-text>
      <transition-group type="transition" :name="!drag ? 'flip-list' : null">
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
      </transition-group>
    </v-card-text>
    <v-card-actions>
      <slot name="actions" />
    </v-card-actions>
    {{ query }}
  </v-card>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import ConditionRule from './ConditionRule'
import { rules } from "./rules"
export default {
  name: 'ConditionBuilder',
  components: { ConditionRule },
  props: {
    value: {
      type: Array,
      default: () => []
    },
  },
  data: () => ({
    rules: rules,
    drag: false,
    selectedRule: undefined,
    query: [],
    sub: undefined,
  }),
  created() {
    if (this.rules) this.selectedRule = this.rules[0]
  },
  methods: {
    addRule() {
      const rule = Object.assign({}, this.selectedRule)
      this.query.push(rule)
      this.value.push({ tag: rule.tag, match: undefined, value: null })
      this.$emit('input', this.value)
    },
    updateRule(i) {
      this.value.splice(i, 1, { tag: this.query[i].tag, match: this.query[i].match, value: this.query[i].value })

      this.$emit('input', this.value)
    },
    deleteRule(i) {
      this.query.splice(i, 1)
      this.value.splice(i, 1)
      this.$emit('input', this.value)
    },
    moveRule({ moved: { oldIndex, newIndex } }) {
      this.value.splice(newIndex, 0, this.value.splice(oldIndex, 1)[0])
      this.$emit('input', this.value)
    }
  },
  computed: {
    dragOptions() {
      return {
        animation: 200,
        ghost: 'hidden-drag-ghost-list'
      };
    }
  }
}
</script>
<style>
#hidden-ghost .sortable-drag {
  opacity: 0;
}
</style>
