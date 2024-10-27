<template>
  <Loader ref="loader">
    <div>
      <Breadcrumb
        :router-items="routerItems"
        name="Cart"/>
      <PageTitle
        class="border-bottom pb-4"
        :secondary="`<div class='fs-6 mb-2'>Restaurant: <strong>${instance.table.restaurant?.name}</strong></div>`"
        :primary="`Ordering from Table: <strong>#${instance.table.number}</strong>`"/>

      <div class="row g-5">
        <div class="col">
          <h6 class="fw-bold mb-4 text-uppercase">
            Cart Items <span class="ms-1">({{ totalItems }})</span>
          </h6>
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
          class="col-12 col-lg-4">
          <h6 class="fw-bold mb-4 text-uppercase">
            Cart Summary
          </h6>
          <div class="card rounded-0">
            <div class="card-body">
              <p class="card-text text-uppercase">
                Total Price
              </p>
              <h2 class="fw-normal mb-4">
                {{ $filters.formatCurrency(totalPrice) }}
              </h2>
              <LoadingButton
                class="btn-primary"
                :is-loading="creatingOrder"
                @click="placeOrder">
                Place Order
              </LoadingButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Loader>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Loader from "@/components/Loader.vue";
import PageTitle from "@/components/PageTitle.vue";
import Empty from "@/components/Empty.vue";
import Breadcrumb from "@/components/Breadcrumb.vue";
import LoadingButton from "@/components/LoadingButton.vue";
import Button from "@/components/Button.vue";
import { HttpNotFound, HttpServerError } from "@/store/network";
import ItemIcon from "@/components/ItemIcon.vue";
import CartButtons from "@/components/CartButtons.vue";

export default {
  name: "CartView",
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, ItemIcon, CartButtons },
  data() {
    return {
      instance: {
        table: {}
      },
      localCart: {},
      creatingOrder: false,
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
    routerItems() {
      return [{
        name: this.instance.table.restaurant?.name,
        to: { name: 'table', params: { uid: this.tableUid } }
      }];
    }
  },
  async mounted() {
    try {
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
