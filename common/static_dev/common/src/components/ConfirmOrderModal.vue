<template>
  <div
    id="confirm-order-modal"
    class="modal fade"
    tabindex="-1">
    <div class="modal-dialog modal-xl">
      <Loader ref="loader">
        <form
          method="post"
          class="modal-content"
          @submit.prevent="() => submitOrder('ACCEPTED')">
          <div class="modal-header">
            <h1 class="modal-title text-uppercase fs-5">
              Incoming Order from table <span class="fw-bold">#{{
                order.table.number }}</span>
            </h1>
            <Button
              class="btn-close"
              data-bs-dismiss="modal"/>
          </div>
          <div class="modal-body text-start p-4">
            <h5 class="mb-0">
              Order Summary
            </h5>
            <hr class="my-3 summary-strip">

            <div class="table-responsive">
              <table class="table summary-table border-0 table-sm table-borderless align-middle mb-0">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th class="text-end">
                      Price
                    </th>
                    <th class="text-end">
                      Quantity
                    </th>
                    <th class="text-end">
                      Total Price
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="{menu_item, ...item} in order.items"
                    :key="menu_item.uid">
                    <td colspan="auto">
                      <div class="d-flex align-items-center min-w-200">
                        <ItemIcon :menu-type="menu_item.menu_type"/>
                        <p class="mb-0">
                          {{ menu_item.name }}
                        </p>
                      </div>
                    </td>
                    <td>
                      {{ item.price_type.toTitleCase() }}
                    </td>
                    <td class="text-end">
                      {{ $filters.formatCurrency(item.price) }}
                    </td>
                    <td class="text-end">
                      {{ $filters.formatInteger(item.quantity) }}
                    </td>
                    <td class="text-end">
                      {{ $filters.formatCurrency(item.total_price) }}
                    </td>
                  </tr>
                  <tr>
                    <td colspan="5">
                      <hr class="my-3 summary-strip">
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="fw-bold"
                      colspan="4">
                      Total Price
                    </td>
                    <td class="text-end fw-bold">
                      {{ $filters.formatCurrency(order.total_price) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div
            v-if="order.status == 'ACCEPTED' || order.status == 'MAKING' || order.status == 'PENDING'"
            class="modal-footer justify-content-center">
            <div
              v-if="order.status == 'PENDING'"
              class="d-flex gap-3">
              <LoadingButton
                :is-loading="!!instance.submitting"
                class="btn-success"
                @click="() => submitOrder('ACCEPTED')">
                Accept
              </LoadingButton>
              <LoadingButton
                :is-loading="!!instance.submitting"
                class="btn-danger"
                @click="() => submitOrder('REJECTED')">
                Reject
              </LoadingButton>
            </div>
            <LoadingButton
              v-else
              :is-loading="!!order.submitting"
              :class="`btn-${badgeClass[getNextStatus(order.status)]}`"
              @click="() => submitOrder(getNextStatus(order.status))">
              Change to {{ getNextStatus(order.status).toTitleCase() }}
            </LoadingButton>
          </div>
        </form>
      </Loader>
    </div>
  </div>
</template>

<script>
import Button from './Button.vue';
import LoadingButton from './LoadingButton.vue';
import ItemIcon from './ItemIcon.vue';
import Loader from './Loader.vue';

export default {
  name: "ConfirmOrderModal",
  components: { Button, LoadingButton, ItemIcon, Loader },
  props: {
    order: {
      type: Object,
      required: true,
    },
  },
  emits: ['closed', 'submit',],
  data() {
    return {
      modalEl: null,
      instance: {},
      badgeClass: {
        PENDING: "info",
        ACCEPTED: "primary",
        REJECTED: "danger",
        MAKING: "warning",
        COMPLETED: "success",
      },
    };
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
    async submitOrder(status = "ACCEPTED") {
      this.instance.status = status;
      this.$emit('submit', this.instance);
    },
    getNextStatus(status) {
      return {
        ACCEPTED: "MAKING",
        MAKING: "COMPLETED",
      }[status];
    },
  }
};
</script>
