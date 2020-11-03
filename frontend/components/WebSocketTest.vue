<template>
  <div>
    hello
    <v-btn @click="sendMessage(test)">
      Send Message
    </v-btn>
    <v-btn @click="getMessage">
      Get Message
    </v-btn>
  </div>
</template>

<script>
export default {
  data() {
    return {
      connection: null,
      test: 'hello world',
      socketResponse: undefined
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
    },
    getMessage() {
      this.socket.emit('getMessage', { id: 'abc123' }, res => {
        this.socketResponse = res
        console.log(res)
      })
    }
  },
  created() {
    // try with nuxt websocket package
    this.socket = this.$nuxtSocket({
      name: 'test',
      // channel: '/index'
      channel: '/dicom/test'
    })

    // try with mdn websockets
    // console.log('Starting Connection')
    // // this.connection = new WebSocket('wss://echo.websocket.org')
    // this.connection = new WebSocket('wss://localhost:5000/dicom/test')
    // console.log(this.connection)
    // console.log(this.connection.readyState)
    // this.connection.onopen = function(event) {
    //   console.log('connected!!!!')
    // }
    // this.connection.onmessage = function(event) {
    //   console.log(event)
    // }
  }
}
</script>
