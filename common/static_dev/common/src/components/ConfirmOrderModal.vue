<template>
  <div
    id="confirm-order-modal"
    class="modal fade"
    tabindex="-1">
    <div class="modal-dialog">
      <Loader ref="loader">
        <form
          method="post"
          class="modal-content"
          @submit.prevent="() => submitOrder('ACCEPTED')">
          <div class="modal-header">
            <h1 class="modal-title text-uppercase fs-5">
              Incoming Order
            </h1>
            <Button
              class="btn-close"
              data-bs-dismiss="modal"/>
          </div>
          <div class="modal-body text-start p-4">
            <h5 class="fw-normal mb-5">
              <span class="fw-bold">{{ order.menu_item?.name }}</span> for table <span class="fw-bold">#{{
                order.table.number }}</span>
            </h5>
            <h6 class="mb-0">
              Order Summary
            </h6>
            <hr class="my-3 summary-strip">

            <div class="table-responsive">
              <table class="table summary-table border-0 table-sm table-borderless align-middle">
                <tbody>
                  <tr>
                    <td>Item</td>
                    <td>{{ order.menu_item?.name }}</td>
                  </tr>
                  <tr>
                    <td>Table</td>
                    <td>#{{ order.table.number }}</td>
                  </tr>
                  <tr>
                    <td>Type</td>
                    <td>{{ order.price_type.toTitleCase() }}</td>
                  </tr>
                  <tr>
                    <td>Quantity</td>
                    <td>{{ order.quantity }}</td>
                  </tr>
                  <tr>
                    <td>Price</td>
                    <td>{{ $filters.formatCurrency(order.price) }}</td>
                  </tr>
                  <tr>
                    <td colspan="2">
                      <hr class="my-3 summary-strip">
                    </td>
                  </tr>
                  <tr>
                    <td>Total Price</td>
                    <td>{{ $filters.formatCurrency(order.total_price) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="modal-footer justify-content-center">
            <LoadingButton
              :is-loading="!!instance.submitting"
              class="btn-success"
              btn-type="submit">
              Accept
            </LoadingButton>
            <LoadingButton
              :is-loading="!!instance.submitting"
              class="btn-danger"
              @click="() => submitOrder('REJECTED')">
              Reject
            </LoadingButton>
          </div>
        </form>
      </Loader>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Button from './Button.vue';
import LoadingButton from './LoadingButton.vue';
import Loader from './Loader.vue';

export default {
  name: "ConfirmOrderModal",
  components: { Button, LoadingButton, Loader },
  props: {
    order: {
      type: Object,
      required: true,
    },
  },
  emits: ['closed', 'submit',],
  data() {
    return { modalEl: null, instance: {}};
  },
  computed: {
    ...mapState(["user"]),
  },
  mounted() {
    this.$refs.loader.complete();
    this.modalEl = document.getElementById('confirm-order-modal');
    this.modal = new window.bootstrap.Modal(this.modalEl, { backdrop: 'static', keyboard: true });
    this.modalEl.addEventListener('hidden.bs.modal', () => this.$emit('closed'));
    if (this.modal) {
      this.modal.show();
    }
    this.instance = { ...this.instance, ...this.order };
  },
  beforeUnmount() {
    if (this.modal) {
      this.modal.hide();
    }
  },
  methods: {
    ...mapActions(['listRestaurant', 'createOrder', 'updateOrder']),
    async submitOrder(status = "ACCEPTED") {
      this.instance.status = status;
      this.$emit('submit', this.instance);
    }
  }
};
</script>
