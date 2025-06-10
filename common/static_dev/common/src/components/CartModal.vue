<template>
  <div
    id="cart-modal"
    class="modal fade modal-lg"
    tabindex="-1">
    <div class="modal-dialog">
      <Loader ref="loader">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-uppercase">
              Cart Items <span class="ms-1">({{ totalItems }})</span>
            </h5>
            <Button
              class="btn-close"
              data-bs-dismiss="modal"/>
          </div>

          <div class="modal-body">
            <Empty
              v-if="!totalItems"
              title="No Items"
              text="You don't have any items in your Cart."
              icon="fas fa-face-frown"/>
            <div
              v-else
              class="table-responsive">
              <table class="table align-middle">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th class="text-end">
                      Price
                    </th>
                    <th class="text-end"/>
                    <th class="text-end">
                      Total Price
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="({ menu_item, price, price_type, quantity }, key) in cart"
                    :key="key">
                    <td colspan="auto">
                      <div class="d-flex align-items-center min-w-200">
                        <ItemIcon :menu-type="menu_item.menu_type"/>
                        <p class="mb-0">
                          {{ menu_item.name }}
                        </p>
                      </div>
                      <small
                        v-if="menu_item.description"
                        class="mt-2 fw-light">{{ menu_item.description }}</small>
                      <div
                        v-if="menu_item.ingredients"
                        class="fw-light text-muted small mt-1">
                        <strong>Ingredients:</strong> {{ menu_item.ingredients }}
                      </div>
                    </td>
                    <td>
                      {{ price_type.toTitleCase() }}
                    </td>
                    <td class="text-end">
                      {{ $filters.formatCurrency(price) }}
                    </td>
                    <td class="text-end">
                      <CartButtons
                        :value="quantity ?? 0"
                        :available="menu_item.available"
                        @add="() => addItem(menu_item, price_type)"
                        @remove="() => removeItem(menu_item, price_type)"/>
                    </td>
                    <td class="text-end">
                      {{ $filters.formatCurrency(price * quantity) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div
            v-if="totalItems"
            class="modal-footer border-top-0 pt-0 flex-column align-items-stretch">
            <div class="d-flex justify-content-between align-items-center fw-medium fs-5 text-dark mb-3">
              <div class="text-uppercase">
                Total Price
              </div>
              <div>
                {{ $filters.formatCurrency(totalPrice) }}
              </div>
            </div>
            <LoadingButton
              class="btn-primary"
              :is-loading="creatingOrder"
              @click="placeOrder">
              Place Order
            </LoadingButton>
          </div>
        </div>
      </Loader>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Loader from "@/components/Loader.vue";
import Empty from "@/components/Empty.vue";
import LoadingButton from "@/components/LoadingButton.vue";
import Button from "@/components/Button.vue";
import { HttpNotFound, HttpServerError } from "@/store/network";
import ItemIcon from "@/components/ItemIcon.vue";
import CartButtons from "@/components/CartButtons.vue";

export default {
  name: "CartModal",
  components: {  Loader, Empty, Button, LoadingButton, ItemIcon, CartButtons },
  emits: ['closed'],
  data() {
    return {
      instance: {
        table: {}
      },
      localCart: {},
      creatingOrder: false,
      modal: null,
      modalEl: null,
    };
  },
  computed: {
    ...mapState(["cart"]),
    tableUid() {
      return this.$route.params.tableUid;
    },
    totalItems() {
      return Object.values(this.cart).reduce((sum, { quantity }) => sum + quantity, 0);
    },
    totalPrice() {
      return Object.values(this.cart).reduce((sum, { quantity, price }) => sum + quantity * price, 0);
    },
  },
  async mounted() {
    try {
      this.modalEl = document.getElementById('cart-modal');
      this.modal = new window.bootstrap.Modal(this.modalEl, { backdrop: 'static', keyboard: true });
      this.modalEl.addEventListener('hidden.bs.modal', () => this.$emit('closed'));
      if (this.modal) {
        this.modal.show();
      }
      this.instance = await this.getCart(this.tableUid);
      this.localCart = this.cart;
    } catch (error) {
      console.error(error);
      let message = error?.data?.detail ?? "Error fetching Table!!";
      if (error instanceof HttpNotFound) {
        this.instance.notFound = true;
        message = error.data?.detail ?? "Table not found!!";
      } else if (error instanceof HttpServerError) {
        message = this.error.message;
      }
      this.$toast.error(message);
    } finally {
      this.$refs.loader.complete();
    }
  },
  beforeUnmount() {
    if (this.modal) {
      this.modal.hide();
    }
  },
  methods: {
    ...mapActions(['getCart', 'setCart', 'addCartItem', 'removeCartItem', 'createTableOrder']),
    addItem(item, price_type = 'FULL') {
      try {
        item.price_type = price_type;
        this.addCartItem(item);
      } catch (error) {
        this.$toast.error("Error adding Menu Item!!");
        console.error(error);
      }
    },
    removeItem(item, price_type = 'FULL') {
      try {
        this.removeCartItem({ item, priceTypes: [price_type] });
      } catch (error) {
        this.$toast.error("Error removing Menu Item!!");
        console.error(error);
      } finally {
        item.removing = false;
      }
    },
    async placeOrder() {
      try {
        this.creatingOrder = true;
        await this.createTableOrder(this.tableUid);
        this.$toast.success("Order placed!!");
        this.setCart({});
        this.$router.push({name: "table-order", params: { tableUid: this.tableUid } });
      } catch (error) {
        const message = error?.data?.detail ?? "Error placing Order!!";
        this.$toast.error(message);
        console.error(error);
      } finally {
        this.creatingOrder = false;
      }
    }
  },
};
</script>
