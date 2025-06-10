<template>
  <Loader ref="loader">
    <div class="">
      <header class="py-3 bg-body sticky-top z-2">
        <PageTitle
          class="container border-bottom border-1"
          :secondary="`Ordering from Table: <strong class='text-primary'>#${instance.table.number}</strong>`"
          :primary="instance.table.restaurant?.name">
          <template #right>
            <Button
              v-if="totalPrice"
              class="d-none d-sm-block btn-primary"
              btn-icon="fa fa-bowl-food me-2"
              @click="isCartOpen = true">
              Items ({{ $filters.formatCurrency(totalPrice) }})
            </Button>
            <router-link
              v-else
              class="d-none d-sm-block btn btn-primary"
              :to="{ name: 'table-order' }">
              <i class="fa fa-bowl-food me-2"/>
              Orders
            </router-link>
          </template>
        </PageTitle>
      </header>

      <div class="container">
        <div class="row g-0 flex-grow-1">
          <div class="col-md-3 d-none d-md-block sticky-sidebar">
            <h5 class="fw-bold text-dark mb-4 border-bottom pb-2">
              Menu Categories
            </h5>
            <nav
              :key="instance.categories"
              class="nav flex-column">
              <Button
                v-for="({ category, ...item }) in instance.categories"
                :key="category.name"
                :class="{ 'fw-medium bg-primary-subtle text-primary': activeCategory === category.uid, 'text-dark': activeCategory !== category.uid }"
                class="text-start fw-light nav-link py-2 px-3 cursor-pointer transition-colors duration-200"
                @click="scrollToCategory(category.uid)">
                {{ category.name }} ({{ item.menu_items_count }})
              </Button>
            </nav>
          </div>

          <main class="col-md-9 ps-md-3 ps-lg-4 pb-5">
            <div>
              <Input
                v-model="searchTerm"
                type="search"
                class="mb-5"
                placeholder="Search for dishes or drinks..."
                icon="fas fa-search"
                @input="searchItem"/>

              <Empty
                v-if="!instance.categories.length"
                title="No Categories"
                text="You don't have any categories for this restaurant."
                icon="fas fa-face-frown"/>
              <section
                v-for="category in instance.categories"
                v-else
                :id="`category-${category.category.uid}`"
                :key="category.category.uid"
                class="mb-4">
                <h4 class="mb-1 fw-normal">
                  {{ category.category.name }}
                </h4>
                <div
                  v-for="item in category.menu_items"
                  :key="item.uid">
                  <div class="card bg-body h-100 border-0 d-flex flex-row px-0 py-3">
                    <div class="flex-shrink-0 me-3">
                      <ItemImage :item="item"/>
                    </div>

                    <div class="flex-grow-1 py-2 row">
                      <div class="col-12 col-sm-8">
                        <div class="d-flex gap-3">
                          <h6 class="card-title fw-normal">
                            {{ item.name }}
                          </h6>
                          <ItemIcon :menu-type="item.menu_type"/>
                        </div>
                        <div class="text-danger mb-2">
                          <span v-if="parseFloat(item.half_price)">
                            {{ $filters.formatCurrency(item.half_price) }} /
                          </span>
                          <span>{{ $filters.formatCurrency(item.full_price) }}</span>
                        </div>
                        <p
                          v-if="item.description"
                          class="card-text fw-light text-muted small mb-1">
                          {{ item.description }}
                        </p>

                        <p
                          v-if="item.ingredients"
                          class="card-text fw-light text-muted small mb-0">
                          <strong>Ingredients:</strong> {{ item.ingredients }}
                        </p>
                      </div>

                      <div class="col text-sm-end">
                        <CartButtons
                          class="w-100"
                          :value="getQuantity(item)"
                          :available="item.available"
                          @add="() => preAddItem(item)"
                          @remove="() => removeItem(item)"/>
                      </div>
                    </div>
                  </div>
                </div>
                <hr>
              </section>
            </div>
          </main>
        </div>

        <div class="fixed-bottom d-sm-none bg-primary text-white p-3 shadow-lg rounded-top-3 z-3">
          <div
            v-if="totalPrice"
            class="d-flex justify-content-between align-items-center">
            <span class="fw-medium">Items ({{ $filters.formatCurrency(totalPrice) }})</span>
            <Button
              class="btn-light text-primary"
              @click="isCartOpen = true">
              View Cart
            </Button>
          </div>
          <router-link
            v-else
            class="btn btn-light text-primary w-100"
            :to="{ name: 'table-order' }">
            <i class="fa fa-bowl-food me-2"/>
            Orders
          </router-link>
        </div>

        <CartFormModal
          v-if="isItemFormOpen"
          :item="cartItem"
          @saved="saveItem"/>

        <CartModal
          v-if="isCartOpen"
          @closed="isCartOpen = false"/>
      </div>
    </div>
  </Loader>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Loader from "@/components/Loader.vue";
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
import Input from '@/components/Input.vue';
import ItemImage from "@/components/ItemImage.vue";
import CartModal from "@/components/CartModal.vue";
import PageTitle from "@/components/PageTitle.vue";

export default {
  name: "TableView",
  components: { Loader, Empty, Button, Breadcrumb, PageTitle, LoadingButton, CategoryFormModal, CategoryCard, CartFormModal, ItemIcon, CartButtons, Input, ItemImage, CartModal },
  data() {
    return {
      instance: {
        categories: [],
        table: {}
      },
      isItemFormOpen: false,
      isCartOpen: false,
      activeCategory: null,
      cartItem: {},
      searchTerm: "",
      timer: null,
      observers: [],
    };
  },
  computed: {
    ...mapState(["cart"]),
    tableUid() {
      return this.$route.params.tableUid;
    },
    totalPrice() {
      return Object.values(this.cart).reduce((sum, { quantity, price }) => sum + quantity * price, 0);
    }
  },
  async mounted() {
    this.searchTerm = this.$route.query.search ?? "";
    await this.fetchDetails();
    this.$refs.loader.complete();
    this.$nextTick(() => {
      this.setupIntersectionObserver();
    });
  },
  unmounted() {
    this.observers.forEach(observer => observer.disconnect());
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
        this.isItemFormOpen = true;
      }
    },
    saveItem(item) {
      this.addItem(item);
      this.isItemFormOpen = false;
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
        this.removeCartItem({ item });
      } catch (error) {
        this.$toast.error("Error removing Menu Item!!");
        console.error(error);
      } finally {
        item.removing = false;
      }
    },
    async searchItem(e) {
      if (this.timer) {
        clearTimeout(this.timer);
      }
      this.searchTerm = e.target.value;
      this.$router.replace({
        query: {
          search: this.searchTerm
        },
      });
      this.timer = setTimeout(async () => {
        await this.fetchDetails();
      }, 300);
    },
    async fetchDetails() {
      try {
        this.instance = await this.getTableCategory({ uid: this.tableUid, query: { search: this.searchTerm } });

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
      }
    },
    scrollToCategory(uid) {
      const element = document.getElementById(`category-${uid}`);
      if (element) {
        const headerOffset = document.querySelector('header').offsetHeight;
        const totalOffset = headerOffset + 20;

        const elementPosition = element.getBoundingClientRect().top + window.scrollY;
        window.scrollTo({
          top: elementPosition - totalOffset,
          behavior: 'smooth'
        });
        this.activeCategory = uid;
      }
    },
    setupIntersectionObserver() {
      const options = {
        root: null,
        rootMargin: '-25% 0px -65% 0px',
        threshold: 0,
      };

      this.instance.categories.forEach(({ category }) => {
        const element = document.getElementById(`category-${category.uid}`);
        if (element) {
          const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
              if (entry.isIntersecting) {
                this.activeCategory = category.uid;
              }
            });
          }, options);
          observer.observe(element);
          this.observers.push(observer);
        }
      });
    }
  }
};
</script>
