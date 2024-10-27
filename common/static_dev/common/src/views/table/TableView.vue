<template>
  <Loader ref="loader">
    <div>
      <PageTitle
        class="border-bottom pb-4"
        :secondary="`<div class='fs-6 mb-2'>Restaurant: <strong>${instance.table.restaurant?.name}</strong></div>`"
        :primary="`Ordering from Table: <strong>#${instance.table.number}</strong>`"/>

      <div class="mt-5">
        <h5 class="fw-bold mb-0 text-uppercase">
          Items
        </h5>

        <Empty
          v-if="!instance.categories.length"
          title="No Categories"
          text="You don't have any categories for this restaurant."
          icon="fas fa-face-frown"/>

        <div v-else>
          <div
            v-for="category in instance.categories"
            :key="category.uid"
            class="mt-5 table-responsive">
            <h6 class="fw-bold mb-3 text-uppercase">
              {{ category.category?.name }}
            </h6>
            <table
              class="table table-striped align-middle">
              <thead>
                <tr>
                  <th>Name</th>
                  <th
                    v-if="category.has_half_price"
                    class="text-end">
                    Half Price
                  </th>
                  <th class="text-end">
                    {{ category.has_half_price ? 'Full' : '' }} Price
                  </th>
                  <th class="text-end"/>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in category.menu_items"
                  :key="item.uid">
                  <td>
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
                    v-if="category.has_half_price"
                    class="text-end w-150">
                    {{ $filters.formatCurrency(item.half_price, true) }}
                  </td>
                  <td class="text-end w-150">
                    {{ $filters.formatCurrency(item.full_price) }}
                  </td>
                  <td class="text-end min-w-200">
                    <CartButtons
                      class="w-100"
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
import CategoryFormModal from "@/components/CategoryFormModal.vue";
import { HttpNotFound, HttpServerError } from "@/store/network";
import CategoryCard from "@/components/CategoryCard.vue";
import CartFormModal from "@/components/CartFormModal.vue";
import ItemIcon from "@/components/ItemIcon.vue";
import CartButtons from "@/components/CartButtons.vue";

export default {
  name: "TableView",
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, CategoryFormModal, CategoryCard, CartFormModal, ItemIcon, CartButtons },
  data() {
    return {
      instance: {
        categories: [],
        table: {}
      },
      showCartModal: false,
      cartItem: {},
    };
  },
  computed: {
    ...mapState(["cart"]),
    tableUid() {
      return this.$route.params.tableUid;
    },
  },
  async mounted() {
    try {
      this.instance = await this.getTableCategory(this.tableUid);
    } catch (error) {
      console.error(error);
      let message = "Error fetching Table!!";
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
    ...mapActions(['getTableCategory', 'setCart', 'addCartItem', 'removeCartItem']),
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
  }
};
</script>
