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
                <th>Next Step</th>
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
                v-for="({ menu_item, table, ...order }) in orderData.results"
                :key="order.uid">
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
                    :class="`bg-${badgeClass[order.status]}`">
                    {{ order.status }}
                  </span>
                </td>
                <td>
                  <LoadingButton
                    v-if="order.status == 'ACCEPTED' || order.status == 'MAKING'"
                    :is-loading="!!order.submitting"
                    class="w-100 text-uppercase p-1 rounded-pill btn-sm"
                    :class="`btn-${badgeClass[getNextStatus(order.status)]}`"
                    @click="() => submitOrder({...order, status: getNextStatus(order.status)})">
                    Change to {{ getNextStatus(order.status) }}
                  </LoadingButton>
                  <div
                    v-if="order.status == 'PENDING'"
                    class="d-flex gap-1">
                    <LoadingButton
                      :is-loading="!!instance.submitting"
                      class="w-100 text-uppercase p-1 rounded-pill btn-sm btn-success"
                      @click="() => submitOrder({...order, status: 'ACCEPTED'})">
                      Accept
                    </LoadingButton>
                    <LoadingButton
                      :is-loading="!!instance.submitting"
                      class="w-100 text-uppercase p-1 rounded-pill btn-sm btn-danger"
                      @click="() => submitOrder({...order, status: 'REJECTED'})">
                      Reject
                    </LoadingButton>
                  </div>
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
      <ConfirmOrderModal
        v-if="newOrder"
        :order="instance ?? {}"
        @submit="submitOrder"/>
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
import { HttpNotFound, HttpServerError, HttpBadRequestError } from "@/store/network";
import ItemIcon from "@/components/ItemIcon.vue";
import CartButtons from "@/components/CartButtons.vue";
import ConfirmOrderModal from "@/components/ConfirmOrderModal.vue";

export default {
  name: 'DashboardOrderView',
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, ItemIcon, CartButtons, ConfirmOrderModal },
  data() {
    return {
      connection: null,
      newOrder: false,
      instance: {},
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
    restaurantUid() {
      return this.$route.params.uid;
    },
    limit() {
      return 4;
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
    getNextStatus(status) {
      return {
        ACCEPTED: "MAKING",
        MAKING: "COMPLETED",
      }[status];
    },
    async fetchOrders() {
      try {
        this.orderData.loading = true;
        const response = await this.listOrder({ table__restaurant__uid: this.restaurantUid, limit: this.limit, offset: this.orderData.page++ * this.limit });
        // this.instance = response.results[0];
        // this.newOrder = true;
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
      this.connection = await this.orderWebsocket(this.restaurantUid);
      this.connection.onmessage = this.updateOrder;
      this.connection.onerror = (event) => {
        console.error(event);
      };
    },
    async submitOrder(order) {
      try {
        order.submitting = true;
        // order.status = this.getNextStatus(order.status);
        this.connection.send(JSON.stringify(order));
      } catch (error) {
        if (error instanceof HttpBadRequestError) {
          this.errors = error.data;
        }
        this.$toast.error("Error updating Order!!");
        console.error(error);
      } finally {
        order.submitting = false;
        this.newOrder = false;
      }
    },
    updateOrder(e) {
      const data = JSON.parse(e.data);
      this.instance = data;
      this.newOrder = true;
      this.orderData.results = this.orderData.results?.map(order => {
        if (data.uid === order.uid) {
          this.newOrder = data.quantity !== order.quantity;
          return data;
        }
        return order;
      });
      if (this.newOrder) {
        this.orderData = {
          results: [],
          page: 0,
          loading: false,
        };
        this.fetchOrders();
      }
      this.$toast.success(`Order ${data.menu_item?.name} updated!!`);
    },
    async send() {
    }
  }
};
</script>
