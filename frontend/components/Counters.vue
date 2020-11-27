<template>
  <v-card
    class="my-1 px-2 text-center"
    height="150"
    width="175"
    elevation="10"
  >
    <v-row align="center">
      <v-col>
        <div
          :class="`${fontsize} font-weight-light`"
          v-text="displayNumber"
        />
        <div class="title white--text" v-text="name" style="position: relative; bottom: 0;"/>
      </v-col>
    </v-row>
  </v-card>

</template>

<script>
export default {
  name: 'Counters',
  props: {
    number: {type: Number, default: 0},
    name: {type: String, default: ''},
    speed: {type: Number, default: 30}
  },
  data: function () {
    return {
      displayNumber: 0,
      interval: false
    }
  },
  computed: {
    fontsize: ctx => {
      const length = ctx.displayNumber.toString().length
      if (length <= 3) return 'text-h1'
      else if (length <= 5) return 'text-h2'
      else if (length <= 6) return 'text-h3'
      else if (length <= 9) return 'text-h4'
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
        this.speed
      )
    }
  },
  beforeDestroy() {
    clearInterval(this.interval)
  },
}
</script>
