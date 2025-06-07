<template>
  <Loader ref="loader">
    <div class="container">
      <Breadcrumb
        :router-items="routerItems"
        name="Order"/>
      <header class="pb-3 bg-body sticky-top z-2">
        <div class="container flex-wrap border-bottom py-4 border-1 d-flex gap-3 align-items-center justify-content-between">
          <div>
            <h1 class="h3 fw-medium text-dark mb-1">
              {{ instance.table.restaurant?.name }}
            </h1>
            <p class="mb-0 text-uppercase">
              Ordering from Table: <span class="fw-medium text-primary">{{ instance.table.number }}</span>
            </p>
          </div>

          <div class="d-flex align-items-center gap-3">
            <span class="fs-6 fw-normal">ORDERS ({{ totalItems }})</span>
            <span class="fs-4 fw-medium text-primary">{{ $filters.formatCurrency(instance.total_price) }}</span>
          </div>
        </div>
      </header>
      <div class="mb-5">
        <Empty
          v-if="!totalItems"
          title="No Items"
          text="You don't have any Orders."
          icon="fas fa-face-frown"/>
        <div
          v-else
          id="orderAccordion"
          class="accordion">
          <div
            v-for="(order, idx) in instance.orders"
            :key="order.uid"
            class="accordion-item border-top border-1 mb-4">
            <h2 class="accordion-header">
              <button
                class="accordion-button shadow-sm"
                type="button"
                data-bs-toggle="collapse"
                :data-bs-target="`#orderCollapse-${idx}`">
                ID: #{{ idx + 1 }}
                <span
                  class="ms-5 p-2 badge rounded-pill"
                  :class="`bg-${badgeClass[order.status]}`">{{ order.status }}</span>
              </button>
            </h2>
            <div
              :id="`orderCollapse-${idx}`"
              class="accordion-collapse collapse"
              :class="{'show': idx === 0}">
              <div class="accordion-body p-0">
                <div class="table-responsive">
                  <table class="table table-hover mb-0">
                    <thead class="bg-light ">
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
                          <div class="d-flex gap-3 align-items-center min-w-200">
                            <p class="mb-0">
                              {{ menu_item.name }}
                            </p>
                            <ItemIcon :menu-type="menu_item.menu_type"/>
                          </div>
                          <small
                            v-if="menu_item.description"
                            class="mt-2 fw-light">{{ menu_item.description }}</small>
                        </td>
                        <td class="fw-light">
                          {{ item.price_type.toTitleCase() }}
                        </td>
                        <td class="text-end fw-light">
                          {{ $filters.formatCurrency(item.price) }}
                        </td>
                        <td class="text-end fw-light">
                          {{ $filters.formatInteger(item.quantity) }}
                        </td>
                        <td class="text-end">
                          {{ $filters.formatCurrency(item.total_price) }}
                        </td>
                      </tr>
                      <tr>
                        <td
                          class="text-end fw-medium"
                          colspan="4">
                          Total Price:
                        </td>
                        <td class="text-end fw-medium">
                          {{ $filters.formatCurrency(order.total_price) }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
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
  name: 'OrderView',
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, ItemIcon, CartButtons },
  data() {
    return {
      connection: null,
      instance: {
        table: {},
        orders: [],
      },
      badgeClass: {
        PENDING: "info",
        ACCEPTED: "success",
        REJECTED: "danger",
        MAKING: "warning",
        COMPLETED: "primary",
      }
    };
  },
  computed: {
    ...mapState(['cart', 'user']),
    tableUid() {
      return this.$route.params.tableUid;
    },
    totalItems() {
      return this.instance.orders.length;
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
      const [a] = await Promise.all([this.getTableOrder(this.tableUid), this.initWebsocket()]);
      this.instance = a;
    } catch (error) {
      console.error(error);
      let message = error?.data?.detail ?? "Error fetching Orders!!";
      if (error instanceof HttpNotFound) {
        this.instance.notFound = true;
        message = error.data?.detail ?? "Orders not found!!";
      } else if (error instanceof HttpServerError) {
        message = this.error.message;
      }
      this.$toast.error(message);
    } finally {
      this.$refs.loader.complete();
    }
  },
  unmounted() {
    this.disconnect();
  },
  methods: {
    ...mapActions(['getTableOrder', 'orderWebsocket']),
    async disconnect() {
      if (this.connection.readyState === WebSocket.OPEN) {
        this.connection.close(1000);
      }
    },
    async initWebsocket() {
      this.connection = await this.orderWebsocket(this.user.uid);
      this.connection.onmessage = this.updateOrder;
      this.connection.onerror = (event) => {
        console.error(event);
      };
    },
    updateOrder(e) {
      const data = JSON.parse(e.data);
      this.instance.orders = this.instance?.orders.map(order => {
        return data.uid === order.uid ? data : order;
      });
      this.$toast.success(`Order ${data.uid} updated!!`);
    },
    async send() {
    }
  }
};
</script>
