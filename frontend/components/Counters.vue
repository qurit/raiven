<template>
  <div>
    {{ displayNumber }}
  </div>
</template>

<script>
var TWEEN = require('tween.js')

export default {
  name: 'Counters',
  props: { number: { default: 0 } },
  data: function() {
    return {
      displayNumber: 0,
      interval: false
    }
  },

  ready: function() {
    this.displayNumber = this.number ? this.number : 0
  },

  watch: {
    number: function() {
      clearInterval(this.interval)

      if (this.number == this.displayNumber) {
        return
      }

      this.interval = window.setInterval(
        function() {
          if (this.displayNumber != this.number) {
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

<style scoped>
p,
h2 {
  margin: 0;
}

.box {
  max-width: 400px;
  margin: 0 auto;
  border: 1px solid red;
  padding: 1em;
}

.count {
  font-size: 40px;
  text-align: right;
  padding: 0.25em 0.5em;
  background-color: #333;
  color: #fff;
  margin-top: 20px;
}

.mode {
  margin-top: 12px;
}

.control {
  position: relative;
}
.reset {
  position: absolute;
  right: 0;
  bottom: 0;
}
</style>
