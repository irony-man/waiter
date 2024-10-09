<template>
  <div
    id="qr-code-full-region"
    class="qr-code"/>
</template>

<script>
// import { Html5QrcodeScanner, Html5QrcodeScannerState } from 'html5-qrcode'

export default {
  name: 'Scanner',
  props: {
    qrbox: {
      type: Number,
      default: 250,
    },
    fps: {
      type: Number,
      default: 10,
    },
  },
  emits: ['scan'],
  data() {
    return {
      html5QrcodeScanner: null,
    };
  },
  async mounted() {
    const config = {
      fps: this.fps,
      qrbox: this.qrbox,
      aspectRatio: 1,
    };
    this.html5QrcodeScanner = new window.Html5QrcodeScanner('qr-code-full-region', config);
    this.html5QrcodeScanner.render(this.onScanSuccess);
    // setTimeout(() => {
    //   document.getElementById('html5-qrcode-button-camera-start').classList.add('btn', 'btn-primary');
    //   document.getElementById('html5-qrcode-button-camera-stop').classList.add('btn', 'btn-primary');
    // }, 3000);
  },
  unmounted() {
    this.html5QrcodeScanner.clear();
  },
  methods: {
    onScanSuccess(decodedText, decodedResult) {
      // if (this.html5QrcodeScanner.currentScanType === 0) {
      //   console.log(this.html5QrcodeScanner.stop());
      //   this.html5QrcodeScanner.stop()
      // }
      this.$emit('scan', decodedText, decodedResult);
      this.html5QrcodeScanner.clear();
    },
  },
};
</script>
