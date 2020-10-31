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
  sockets: {
    connect: function() {
      console.log('socket connected')
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
    // this.connection = new WebSocket('wss://echo.websocket.org')
    this.connection = new WebSocket('wss://localhost:5000/dicom/test')
    console.log(this.connection)
    this.connection.onopen = function(event) {
      console.log('connected!!!!')
    }
    this.connection.onmessage = function(event) {
      console.log(event)
    }
  }
}
</script>
