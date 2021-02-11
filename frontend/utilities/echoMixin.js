import {send_c_echo} from "@/api/dicom";

export default {
  data: () => ({
    loading: false,
    echoIcon: 'mdi-wifi'
  }),
  methods: {
    async sendEcho(node) {
      this.loading = 'accent'

      try {
        await send_c_echo(this, node)
        this.echoIcon = 'mdi-wifi-strength-4'
        this.$toaster.toastSuccess('C-ECHO Succeeded')
      } catch (e) {
        this.echoIcon = 'mdi-wifi-strength-alert-outline'
        this.$toaster.toastError('C-ECHO Failed')
      }

      this.loading = false
    }
  }
}
