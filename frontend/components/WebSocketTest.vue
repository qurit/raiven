<template>
  <div>
    hello
    <v-btn @click="sendMessage(test)">
      Send Message
    </v-btn>
  </div>
</template>

<script>
export default {
  data() {
    return {
      connection: null,
      test: 'hello world'
    }
  },
  methods: {
    sendMessage(message) {
      console.log(this.connection)
      this.connection.send(message)
    }
  },
  created() {
    console.log('Starting Connection')
    this.connection = new WebSocket('wss://echo.websocket.org')
    this.connection.onopen = function(event) {
      console.log(event)
      console.log('Connected to echo websocket server')
    }
    this.connection.onmessage = function(event) {
      console.log(event)
    }
  }
}
</script>
