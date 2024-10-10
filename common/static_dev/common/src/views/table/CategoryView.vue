<template>
  <Loader ref="loader">
    <div class="container my-5">
      <Empty
        v-if="!!instance.notFound"
        title="Category not Found"
        text="The category you are looking for is not in this restaurant."
        icon="fas fa-face-frown"/>
      <div v-else>
        <Breadcrumb
          :router-items="routerItems"
          :name="instance.category?.name"/>
        <PageTitle
          class="border-bottom pb-4"
          :secondary="`<div class='fs-6 mb-2'>Ordering from Table: <strong>#${instance.table.number}</strong> of Restaurant: <strong>${instance.table.restaurant.name}</strong></div>`"
          :primary="instance.category?.name"/>

        <div class="mb-5">
          <h6 class="fw-bold mb-3 text-uppercase">
            Items
          </h6>

          <Empty
            v-if="!instance.menu_items?.length"
            title="No Items"
            text="You don't have any items in this Category."
            icon="fas fa-face-frown"/>

          <div v-else>
            <div class="table-responsive">
              <table class="table table-striped align-middle">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th
                      v-if="showHalfPrice"
                      class="text-end">
                      Half Price
                    </th>
                    <th class="text-end">
                      {{ showHalfPrice ? 'Full' : '' }} Price
                    </th>
                    <th class="text-end"/>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="item in instance.menu_items"
                    :key="item.uid">
                    <td colspan="auto">
                      <div class="d-flex align-items-center min-w-200">
                        <ItemIcon :menu-type="item.menu_type"/>
                        <p class="mb-0">
                          {{ item.name }}
                        </p>
                      </div>
                      <small
                        v-if="item.description"
                        class="mt-2 fw-light">{{ item.description }}</small>
                    </td>
                    <td
                      v-if="showHalfPrice"
                      class="text-end">
                      {{ $filters.formatCurrency(item.half_price, true) }}
                    </td>
                    <td class="text-end">
                      {{ $filters.formatCurrency(item.full_price) }}
                    </td>
                    <td class="text-end">
                      <CartButtons
                        :value="getQuantity(item)"
                        :available="item.available"
                        @add="() => preAddItem(item)"
                        @remove="() => removeItem(item)"/>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <CartFormModal
          v-if="showCartModal"
          :item="cartItem"
          @saved="saveItem"/>
      </div>
    </div>
  </Loader>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Loader from "@/components/Loader.vue";
import PageTitle from "@/components/PageTitle.vue";
import Empty from "@/components/Empty.vue";
import BooleanIcon from "@/components/BooleanIcon.vue";
import Breadcrumb from "@/components/Breadcrumb.vue";
import LoadingButton from "@/components/LoadingButton.vue";
import Button from "@/components/Button.vue";
import { HttpNotFound, HttpServerError } from "@/store/network";
import CartFormModal from "@/components/CartFormModal.vue";
import ItemIcon from "@/components/ItemIcon.vue";
import CartButtons from "@/components/CartButtons.vue";

export default {
  name: "CategoryView",
  components: { PageTitle, Loader, Empty, BooleanIcon, Breadcrumb, LoadingButton, Button, CartFormModal, ItemIcon, CartButtons },
  data() {
    return {
      instance: {},
      cartItem: {},
      showCartModal: false,
    };
  },
  computed: {
    ...mapState(["user", "cart"]),
    categoryUid() {
      return this.$route.params.categoryUid;
    },
    tableUid() {
      return this.$route.params.tableUid;
    },
    showHalfPrice() {
      return this.instance.menu_items.some(m => m.half_price != 0);
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
      this.instance = await this.getTableQRCode({ uid: this.tableUid, query: { category__uid: this.categoryUid } });
    } catch (error) {
      console.error(error);
      let message = error?.data?.detail ?? "Error fetching Table!!";
      if (error instanceof HttpNotFound) {
        this.instance.notFound = true;
        message = error.data?.detail ?? "Category not found!!";
      } else if (error instanceof HttpServerError) {
        message = this.error.message;
      }
      this.$toast.error(message);
    } finally {
      this.$refs.loader.complete();
    }
  },
  methods: {
    ...mapActions(['getTableQRCode', 'setCart', 'addCartItem', 'removeCartItem']),
    getQuantity(item) {
      return ['HALF', 'FULL'].reduce((sum, t) => {
        const key = `${item.uid}/${t}`;
        return key in this.cart ? sum + this.cart[key].quantity : sum;
      }, 0);
    },
    preAddItem(item) {
      if (item.half_price == parseFloat(0)) {
        item.price_type = 'FULL';
        this.addItem(item);
      } else {
        this.cartItem = item;
        this.showCartModal = true;
      }
    },
    saveItem(item) {
      this.addItem(item);
      this.showCartModal = false;
    },
    addItem(item) {
      try {
        this.addCartItem(item);
      } catch (error) {
        this.$toast.error("Error adding Menu Item!!");
        console.error(error);
      }
    },
    removeItem(item) {
      try {
        this.removeCartItem({item});
      } catch (error) {
        this.$toast.error("Error removing Menu Item!!");
        console.error(error);
      } finally {
        item.removing = false;
      }
    }
  },
};
</script>
