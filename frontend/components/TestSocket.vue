<template>
  <v-sheet height="100">
    <v-row no-gutters justify="center" align="center" style="height: inherit">
      <v-btn @click="getMessage" outlined color="primary">TEST SOCKET</v-btn>
    </v-row>

    {{ messageRxd }}
  </v-sheet>
</template>

<script>
export default {
  name: "TestSocket",
  data: () => ({
    messageRxd: 'not got'
  }),
  mounted() {
    this.socket = this.$nuxtSocket({ })
  },
  methods: {
    getMessage() {
        this.socket.emit('getMessage', { id: 'abc123' }, (resp) => {
        this.messageRxd = resp
      })
    }
  }
}
</script>
