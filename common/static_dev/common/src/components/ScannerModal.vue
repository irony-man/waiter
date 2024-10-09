<template>
  <div
    id="scanner-modal"
    class="modal fade"
    tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">
            Scanner
          </h1>
        </div>
        <div class="modal-body">
          <Scanner @scan="(decodedText, decodedResult) => $emit('scan', decodedText, decodedResult)"/>
        </div>
        <div class="modal-footer justify-content-start">
          <Button
            class="btn-secondary"
            data-bs-dismiss="modal">
            Close
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Scanner from './Scanner.vue';
import Button from './Button.vue';

export default {
  name: "ScannerModal",
  components: {Scanner, Button},
  emits: ['closed', 'scan'],
  data() {
    return { modalEl: null };
  },
  mounted() {
    this.modalEl = document.getElementById('scanner-modal');
    this.modal = new window.bootstrap.Modal(this.modalEl, { backdrop: 'static', keyboard: true });
    this.modalEl.addEventListener('hidden.bs.modal', () => this.$emit('closed'));
    if (this.modal) {
      this.modal.show();
    }
  },
  beforeUnmount() {
    if (this.modal) {
      this.modal.hide();
    }
  },
};
</script>
