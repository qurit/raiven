<template>
  <div>
    <SocketStatus :status="socketStatus" />
     <v-btn @click="sendMessage">
      Send Message
    </v-btn>
    {{ messageRxd }}
  </div>
</template>

<script>
  import SocketStatus from 'nuxt-socket-io/components/SocketStatus.vue'
export default {
  components: {
    SocketStatus
  },
  data() {
    return {
      socket: null,
      test: 'hello world',
      socketStatus: {}, // simply define this, and it will be populated with the status
      messageRxd: []
    }
  },
  methods: {
    sendMessage() {
      this.socket.emit('message', {data: 'hello from nuxt'}, (resp, data) => {
        console.log(resp, data)
        this.messageRxd.push(data)
      })
    }
  },
  mounted() {
    this.socket = this.$nuxtSocket({path: '/ws/socket.io'})
  }
}
</script>
