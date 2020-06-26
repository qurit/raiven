<template>
  <v-sheet>
    <v-row no-gutters justify="center" align="center" style="height: inherit">
      <v-btn @click="getMessage" outlined color="primary">TEST SOCKET</v-btn>
    </v-row>
    <SocketStatus :status="socketStatus" />

    {{ messageRxd }}
  </v-sheet>
</template>

<script>
import SocketStatus from 'nuxt-socket-io/components/SocketStatus.vue'

export default {
  name: "TestSocket",
  components: {
    SocketStatus
  },
  data() {
    return {
      socketStatus: {}, // simply define this, and it will be populated with the status
      messageRxd: 'no'
    }
  },
  mounted() {
    this.socket = this.$nuxtSocket({})
    this.socket.on('my_response', (msg) => {
      console.log(msg)
      this.messageRxd = msg
    });


  },
  methods: {
    getMessage() {
      this.socket.emit('my_event', {data: 'hello from nuxt'}, (resp) => {
        this.messageRxd = resp
      })
    }
  }
}
</script>
