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
                v-for="({ menu_item, price, price_type, quantity, total_price }, key) in instance.orders"
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
                  {{ $filters.formatInteger(quantity) }}
                </td>
                <td class="text-end">
                  {{ $filters.formatCurrency(total_price) }}
                </td>
              </tr>
              <tr>
                <td
                  class="fw-bold"
                  colspan="4">
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

export default {
  name: 'OrderView',
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, ItemIcon, CartButtons },
  data() {
    return {
      connection: null,
      data: null,
      instance: {
        table: {},
        orders: [],
      },
      breadcrumb: [
        { label: 'Manufacturing', link: '/manufacturing/' },
        { label: 'Live Schedule' },
      ],
    };
  },
  computed: {
    ...mapState(['cart']),
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
      // this.initWebsocket();
      this.instance = await this.getOrder(this.tableUid);
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
    ...mapActions(['getOrder']),
    async disconnect() {
      if (this.connection.readyState === WebSocket.OPEN) {
        this.connection.close(1000);
      }
    },
    initWebsocket() {
      this.connection = new WebSocket(`ws://localhost:8000/ws/order/84ca50ef-7dc8-40de-ae43-1c402e59d6ef/`);

      this.connection.onopen = () => {
        console.log('WebSocket connected');
      };

      this.connection.onerror = (event) => {
        console.error(event);
      };

      this.connection.onclose = () => {
        console.log('WebSocket closed');
      };

      this.connection.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);
      };
    },
    async send() {
    }
  }
};
</script>
