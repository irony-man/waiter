<template>
  <Loader ref="loader">
    <div>
      <Breadcrumb
        :router-items="routerItems"
        name="Order"/>
      <PageTitle
        class="border-bottom pb-4"
        :secondary="`<div class='fs-6 mb-2'>Restaurant: <strong>${instance.table.restaurant?.name}</strong></div>`"
        :primary="`Orders from Table: <strong>#${instance.table.number}</strong>`"/>

      <div class="mb-5">
        <h6 class="fw-bold mb-4 text-uppercase">
          Orders <span class="ms-1">({{ totalItems }})</span>
        </h6>
        <Tabs/>
        <Empty
          v-if="!totalItems"
          title="No Items"
          text="You don't have any Orders."
          icon="fas fa-face-frown"/>
        <div
          v-else
          class="table-responsive">
          <table class="table align-middle">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Status</th>
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
                v-for="({ menu_item, ...order }, key) in instance.orders"
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
                  {{ order.price_type.toTitleCase() }}
                </td>
                <td>
                  <span
                    class="w-100 p-2 badge rounded-pill"
                    :class="`bg-${badgeClass[order.status]}`">{{ order.status }}</span>
                </td>
                <td class="text-end">
                  {{ $filters.formatCurrency(order.price) }}
                </td>
                <td class="text-end">
                  {{ $filters.formatInteger(order.quantity) }}
                </td>
                <td class="text-end">
                  {{ $filters.formatCurrency(order.total_price) }}
                </td>
              </tr>
              <tr>
                <td
                  class="fw-bold"
                  colspan="5">
                  Total Price
                </td>
                <td class="text-end fw-bold">
                  {{ $filters.formatCurrency(instance.total_price) }}
                </td>
              </tr>
            </tbody>
          </table>
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
import Tabs from "@/components/Tabs.vue";

export default {
  name: 'OrderView',
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, ItemIcon, CartButtons, Tabs },
  data() {
    return {
      connection: null,
      instance: {
        table: {},
        orders: [],
      },
      badgeClass: {
        PENDING: "info",
        ACCEPTED: "primary",
        REJECTED: "danger",
        MAKING: "warning",
        COMPLETED: "success",
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
      this.$toast.success(`Order ${data.menu_item?.name} updated!!`);
    },
    async send() {
    }
  }
};
</script>
