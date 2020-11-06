<template>
  <v-sheet
    :color="color"
    class="pa-2 text-center"
    height="150"
    width="150"
    dark
  >
    <div
      :class="`${fontsize} display-4 font-weight-light white--text`"
      v-text="displayNumber"
    />
    <div class="title white--text" v-text="name" />
  </v-sheet>
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

  // ready: function() {
  //   this.displayNumber = this.number ? this.number : 0
  // },
  computed: {
    fontsize: ctx => {
      const length = ctx.displayNumber.toString().length
      if (length <= 2) return 'display-4'
      else if (length <= 4) return 'display-3'
      else if (length <= 5) return 'display-2'
      else if (length <= 7) return 'display-1'
      else return ''
    }
  },

  watch: {
    number: function() {
      clearInterval(this.interval)

      if (this.number == this.displayNumber) {
        console.log('finished')
        return
      }

      this.interval = window.setInterval(
        function() {
          if (this.displayNumber != this.number) {
            console.log('not finished')
            var change = (this.number - this.displayNumber) / 10

            change = change >= 0 ? Math.ceil(change) : Math.floor(change)

            this.displayNumber = this.displayNumber + change
          }
        }.bind(this),
        20
      )
    }
  }
}
</script>
