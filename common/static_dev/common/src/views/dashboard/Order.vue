<template>
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

      <Loader ref="orderLoader">
        <Empty
          v-if="!orderData.results.length"
          title="No Items"
          text="You don't have any Orders."
          icon="fas fa-face-frown"/>
        <div
          v-else
          id="orderAccordion"
          class="accordion">
          <div
            v-for="(order, idx) in orderData.results"
            :key="order.uid"
            class="accordion-item">
            <h2 class="accordion-header">
              <div
                class="text-uppercase accordion-button"
                type="button"
                data-bs-toggle="collapse"
                :data-bs-target="`#orderCollapse-${idx}`">
                <div class="row w-100">
                  <div class="col">
                    Order from table: #{{ order.table.number }}
                  </div>
                  <div class="col">
                    <span
                      class="ms-5 p-2 badge rounded-pill"
                      :class="`bg-${badgeClass[order.status]}`">{{ order.status }}</span>
                  </div>
                </div>
              </div>
            </h2>
            <div
              :id="`orderCollapse-${idx}`"
              class="accordion-collapse collapse"
              :class="{'show': order.status !== 'COMPLETED'}">
              <div
                v-if="order.items?.length"
                class="accordion-body table-responsive">
                <table
                  class="table align-middle">
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
                        <small
                          v-if="menu_item.description"
                          class="mt-2 fw-light">{{ menu_item.description }}</small>
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
                <div
                  v-if="showNextStep"
                  class="text-end">
                  <LoadingButton
                    v-if="order.status == 'ACCEPTED' || order.status == 'MAKING'"
                    :is-loading="!!order.submitting"
                    class=" text-uppercase btn-sm"
                    :class="`btn-${badgeClass[getNextStatus(order.status)]}`"
                    @click="() => submitOrder({ ...order, status: getNextStatus(order.status) })">
                    Change to {{ getNextStatus(order.status) }}
                  </LoadingButton>
                  <div
                    v-if="order.status == 'PENDING'"
                    class="d-flex justify-content-end gap-3">
                    <LoadingButton
                      :is-loading="!!instance.submitting"
                      class="text-uppercase btn-sm btn-success"
                      @click="() => submitOrder({ ...order, status: 'ACCEPTED' })">
                      Accept
                    </LoadingButton>
                    <LoadingButton
                      :is-loading="!!instance.submitting"
                      class="text-uppercase btn-sm btn-danger"
                      @click="() => submitOrder({ ...order, status: 'REJECTED' })">
                      Reject
                    </LoadingButton>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
          class="table-responsive">
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
      </Loader>
    </div>
    <ConfirmOrderModal
      v-if="showModal"
      :order="instance ?? {}"
      @submit="submitOrder"
      @closed="showModal = false"/>
  </div>
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
      limit: 48,
    };
  },
  computed: {
    ...mapState(['cart', 'user']),
    restaurantUid() {
      return this.$route.params.uid;
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
      // this.$refs.loader.complete();
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
        this.$refs.orderLoader.start();
        this.orderData.loading = true;
        const response = await this.listOrder({ table__restaurant__uid: this.restaurantUid, limit: this.limit, offset: this.orderData.page++ * this.limit, status: this.selectedTab, ordering: '-created' });
        response.results = [...this.orderData.results, ...response.results];
        this.orderData = { ...this.orderData, ...response };
      } catch (err) {
        this.$toast.error("Error fetching orders!!");
        console.error(err);
      } finally {
        this.$refs.orderLoader.complete();
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
      let oldOrder = false;
      this.orderData.results = this.orderData.results?.map(order => {
        if(data.uid === order.uid) {
          oldOrder = true;
          return data;
        }
        return order;
      });
      if(!oldOrder) {
        this.showModal = true;
        this.orderData.results?.push(data);
        this.limit++;
      }
      this.$toast.success(`Order ${data.uid} updated!!`);
    },
  }
};
</script>
