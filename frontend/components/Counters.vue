<template>
  <v-row class="d-flex justify-center">
    <v-card
      class="ma-1 text-center justify-center"
      height="150"
      width="175"
      elevation="10"
    >
      <div
        :class="`${fontsize} display-4 font-weight-light white--text`"
        v-text="displayNumber"
      />
      <div class="title white--text" v-text="name" />
    </v-card>
  </v-row>
</template>

<script>
var TWEEN = require('tween.js')

export default {
  name: 'Counters',
  props: { number: { default: 0 }, name },
  data: function() {
    return {
      displayNumber: 0,
      interval: false
    }
  },

  computed: {
    fontsize: ctx => {
      const length = ctx.displayNumber.toString().length
      if (length <= 3) return 'display-4'
      else if (length <= 5) return 'display-2'
      else if (length <= 7) return 'display-1'
      else return ''
    }
  },

  watch: {
    number: function() {
      clearInterval(this.interval)

      if (this.number === this.displayNumber) {
        return
      }

      this.interval = window.setInterval(
        function() {
          if (this.displayNumber !== this.number) {
            var change = (this.number - this.displayNumber) / 10
            change = change >= 0 ? Math.ceil(change) : Math.floor(change)
            this.displayNumber = this.displayNumber + change
          }
        }.bind(this),
        // this sets how quickly we increment to reach the displayNumber (higher number means longer delay between each number update)
        30
      )
    }
  }
}
</script>
