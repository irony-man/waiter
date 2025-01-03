<template>
  <Loader ref="loader">
    <div>
      <Breadcrumb
        :router-items="routerItems"
        name="Order"/>
      <PageTitle
        :secondary="`This is where you manage chain <b>${user.chain_name}</b>.`"
        primary="Orders"/>

      <div class="mb-5">
        <Tabs
          v-model="selectedTab"
          :tabs="tabs"
          @update:model-value="onChangeTab"/>
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
                <th v-if="showNextStep">
                  Next Step
                </th>
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
                v-for="order in orderData.results"
                :key="order.uid">
                <td colspan="auto">
                  <div class="d-flex align-items-center min-w-200">
                    <ItemIcon :menu-type="order.menu_item?.menu_type"/>
                    <p class="mb-0">
                      {{ order.menu_item?.name }}
                    </p>
                  </div>
                  <small
                    v-if="order.menu_item?.description"
                    class="mt-2 fw-light">{{ order.menu_item?.description }}</small>
                </td>
                <td class="fw-bold text-end">
                  #{{ order.table?.number }}
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
                <td v-if="showNextStep">
                  <LoadingButton
                    v-if="order.status == 'ACCEPTED' || order.status == 'MAKING'"
                    :is-loading="!!order.submitting"
                    class="w-100 text-uppercase p-1 rounded-pill btn-sm"
                    :class="`btn-${badgeClass[getNextStatus(order.status)]}`"
                    @click="() => submitOrder({ ...order, status: getNextStatus(order.status) })">
                    Change to {{ getNextStatus(order.status) }}
                  </LoadingButton>
                  <div
                    v-if="order.status == 'PENDING'"
                    class="d-flex gap-1">
                    <LoadingButton
                      :is-loading="!!instance.submitting"
                      class="w-100 text-uppercase p-1 rounded-pill btn-sm btn-success"
                      @click="() => submitOrder({ ...order, status: 'ACCEPTED' })">
                      Accept
                    </LoadingButton>
                    <LoadingButton
                      :is-loading="!!instance.submitting"
                      class="w-100 text-uppercase p-1 rounded-pill btn-sm btn-danger"
                      @click="() => submitOrder({ ...order, status: 'REJECTED' })">
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
        v-if="showModal"
        :order="instance ?? {}"
        @submit="submitOrder"
        @closed="showModal = false"/>
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
import Tabs from "@/components/Tabs.vue";

export default {
  name: 'DashboardOrderView',
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, ItemIcon, CartButtons, ConfirmOrderModal, Tabs },
  data() {
    return {
      connection: null,
      showModal: false,
      instance: {},
      defaultState: {
        results: [],
        page: 0,
        loading: false,
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
      },
      selectedTab: '',
    };
  },
  computed: {
    ...mapState(['cart', 'user']),
    restaurantUid() {
      return this.$route.params.uid;
    },
    limit() {
      return 48;
    },
    routerItems() {
      return [{
        name: this.user.chain_name,
        to: { name: 'dashboard' }
      }];
    },
    tabs() {
      return [{ value: '', name: 'All' }, ...this.user.choices.order_status];
    },
    showNextStep() {
      if (this.selectedTab === '') {
        return this.orderData.results.some(o => (o.status === 'ACCEPTED' || o.status === 'PENDING' || o.status === 'MAKING'));
      }
      return this.selectedTab === 'ACCEPTED' || this.selectedTab === 'PENDING' || this.selectedTab === 'MAKING';
    },
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
    onChangeTab() {
      this.orderData = { ...this.defaultState };
      this.fetchOrders();
    },
    async fetchOrders() {
      try {
        this.orderData.loading = true;
        const response = await this.listOrder({ table__restaurant__uid: this.restaurantUid, limit: this.limit, offset: this.orderData.page++ * this.limit, status: this.selectedTab, ordering: '-created' });
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
        this.connection.send(JSON.stringify(order));
      } catch (error) {
        if (error instanceof HttpBadRequestError) {
          this.errors = error.data;
        }
        this.$toast.error("Error updating Order!!");
        console.error(error);
      } finally {
        order.submitting = false;
        this.showModal = false;
      }
    },
    updateOrder(e) {
      const data = JSON.parse(e.data);
      console.log(data);
      this.instance = data;
      this.showModal = false;
      const oldOrder = this.orderData.results?.find(order => data.uid === order.uid);
      if(oldOrder) {
        this.showModal = oldOrder.quantity !== data.quantity;
        oldOrder.quantity = data.quantity;
      }
      else {
        this.showModal = true;
        this.orderData = { ...this.defaultState };
        this.fetchOrders();
      }
      this.$toast.success(`Order ${data.menu_item?.name} updated!!`);
    },
  }
};
</script>
