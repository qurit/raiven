<template>
  <v-sheet>
    <v-row no-gutters justify="center" align="center" style="height: inherit">
      <v-btn @click="getMessage" outlined color="primary">TEST SOCKET</v-btn>
    </v-row>
    <SocketStatus :status="socketStatus"></SocketStatus>

    {{ messageRxd }}
  </v-sheet>
</template>

<script>
import SocketStatus from 'nuxt-socket-io/components/SocketStatus.vue'

export default {
  name: "TestSocket",
  data() {
    return {
      socketStatus: {}, // simply define this, and it will be populated with the status
      badStatus: {}, // Status will be populated here if "statusProp == 'badStatus'"
      messageRxd: 'no'
    }
  },
  mounted() {
    this.socket = this.$nuxtSocket({name: 'goodSocket' })
    this.socket.on('my response', (msg, cb) => {
      this.messageRxd = msg.data
    })
  },
  methods: {
    getMessage() {
      this.socket.emit('message', { id: 'abc123' })
    }
  }
}
</script>
