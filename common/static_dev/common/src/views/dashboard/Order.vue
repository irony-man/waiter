<template>
  <Loader ref="loader">
    <div>
      <Breadcrumb
        :router-items="routerItems"
        name="Order"/>
      <PageTitle
        :secondary="`This is where you manage <b>Chain ${user.chain_name}</b>.`"
        primary="Orders"/>

      <div class="mb-5">
        <Empty
          v-if="!orderData.results.length"
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
                <th class="text-end">
                  Table Number
                </th>
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
                v-for="({ menu_item, table, ...order }, key) in orderData.results"
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
                <td class="fw-bold text-end">
                  #{{ table.number }}
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
            </tbody>
          </table>
          <div
            v-if="orderData.next"
            class="mt-5 text-center">
            <LoadingButton
              :is-loading="!!orderData.loading"
              class="btn-dark"
              btn-type="button"
              @click="fetchOrders()">
              Load More
            </LoadingButton>
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
  name: 'DashboardOrderView',
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, ItemIcon, CartButtons },
  data() {
    return {
      connection: null,
      instance: {
        table: {},
        orders: [],
      },
      orderData: {
        results: [],
        page: 0,
        loading: false,
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
    restaurantUid(){
      return this.$route.params.uid;
    },
    limit() {
      return 30;
    },
    routerItems() {
      return [{
        name: this.user.chain_name,
        to: { name: 'dashboard' }
      }];
    }
  },
  async mounted() {
    try {
      await Promise.all([this.fetchOrders(), this.initWebsocket()]);
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
  unmounted() {
    this.disconnect();
  },
  methods: {
    ...mapActions(['listOrder', 'orderWebsocket']),
    async fetchOrders() {
      try {
        this.orderData.loading = true;
        const response = await this.listOrder({ table__restaurant__uid: this.restaurantUid, limit: this.limit, offset: this.orderData.page++ * this.limit });
        response.results = [...this.orderData.results, ...response.results];
        this.orderData = { ...this.orderData, ...response };
      } catch (err) {
        this.$toast.error("Error fetching orders!!");
        console.error(err);
      } finally {
        this.orderData.loading = false;
      }
    },
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

      this.orderData.results = this.orderData.results?.map(order => {
        if (data.uid === order.uid) {
          order.status = data.status;
        }
        return order;
      });
      this.$toast.success(`Order #${data.uid} updated!!`);
    },
    async send() {
    }
  }
};
</script>
