<template>
  <div
    id="qr-code-full-region"
    class="qr-code"/>
</template>

<script>
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
  },
  unmounted() {
    this.html5QrcodeScanner.clear();
  },
  methods: {
    onScanSuccess(decodedText, decodedResult) {
      this.$emit('scan', decodedText, decodedResult);
      this.html5QrcodeScanner.clear();
    },
  },
};
</script>
