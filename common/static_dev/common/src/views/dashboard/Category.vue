<template>
  <Loader ref="loader">
    <div class="container my-5">
      <Empty
        v-if="!!category.notFound"
        title="Category not Found"
        text="The category you are looking for is not in this restaurant."
        icon="fas fa-face-frown"/>
      <div v-else>
        <Breadcrumb
          :router-items="routerItems"
          :name="category.name"/>
        <PageTitle
          class="border-bottom pb-4"
          :secondary="`A category of <strong>${category.restaurant.name}</strong>`"
          :primary="category.name">
          <template #right>
            <div class="d-flex gap-3 flex-wrap align-items-center">
              <Button
                class="btn-warning"
                btn-icon="fas fa-pen"
                @click="showCategoryForm = true">
                Edit Category
              </Button>
              <LoadingButton
                v-if="!menuItemData.results.length"
                class="btn-outline-danger"
                :is-loading="!!deleting"
                btn-icon="fas fa-trash"
                @click="removeCategory">
                Delete Category
              </LoadingButton>
            </div>
          </template>
        </PageTitle>


        <div class="mb-5">
          <div class="d-flex gap-3 flex-wrap align-items-center mb-5 g-4">
            <div class="flex-grow-1">
              <h6 class="fw-bold mb-0 text-uppercase">
                Items
              </h6>
            </div>

            <Button
              class="btn-primary"
              btn-icon="fas fa-plus"
              @click="() => startEditing(-1)">
              Add Item
            </Button>
          </div>

          <Empty
            v-if="!menuItemData.results.length"
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
                    v-for="(item, idx) in menuItemData.results"
                    :key="item.uid">
                    <td colspan="auto">
                      <div class="d-flex align-items-center">
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
                      {{ $filters.formatCurrency(item.half_price) }}
                    </td>
                    <td class="text-end">
                      {{ $filters.formatCurrency(item.full_price) }}
                    </td>
                    <td class="text-end">
                      <div>
                        <LoadingButton
                          :is-loading="!!item.deleting"
                          btn-icon="fas fa-pen text-warning"
                          @click="() => startEditing(idx)"/>
                        <LoadingButton
                          :is-loading="!!item.deleting"
                          btn-type="button"
                          btn-icon="fas text-danger fa-trash"
                          @click="() => removeItem(item)"/>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div
              v-if="menuItemData.next"
              class="mt-3 text-center">
              <LoadingButton
                :is-loading="!!menuItemData.loading"
                btn-type="button"
                class="btn-primary"
                @click="fetchMenuItems()">
                Load More
              </LoadingButton>
            </div>
          </div>
        </div>
        <MenuItemFormModal
          v-if="showMenuItemForm"
          :menu-item="instance"
          @closed="showMenuItemForm = false"
          @saved="saveItem"/>
        <CategoryFormModal
          v-if="showCategoryForm"
          :category="category"
          @closed="showCategoryForm = false"
          @saved="saveCategory"/>
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
import MenuItemFormModal from "@/components/MenuItemFormModal.vue";
import CategoryFormModal from "@/components/CategoryFormModal.vue";
import { HttpNotFound, HttpServerError } from "@/store/network";
import ItemIcon from "@/components/ItemIcon.vue";

export default {
  name: "CategoryView",
  components: { PageTitle, Loader, Empty, BooleanIcon, Breadcrumb, LoadingButton, Button, MenuItemFormModal, CategoryFormModal, ItemIcon },
  data() {
    return {
      category: {},
      deleting: false,
      showMenuItemForm: false,
      showCategoryForm: false,
      instance: {},
      menuItemData: {
        results: [],
        page: 0,
        loading: false,
      },
    };
  },
  computed: {
    ...mapState(["user"]),
    categoryUid() {
      return this.$route.params.uid;
    },
    limit() {
      return 48;
    },
    showHalfPrice() {
      return this.menuItemData.results.some(m => m.half_price != 0);
    },
    routerItems() {
      return [{
        name: this.user.chain_name,
        to: { name: 'dashboard' }
      }, {
        name: this.category.restaurant?.name,
        to: { name: 'dashboard-restaurant', params: { uid: this.category.restaurant?.uid } }
      }];
    }
  },
  async mounted() {
    await Promise.all([
      this.fetchCategory(),
      this.fetchMenuItems()
    ]);
    this.$refs.loader.complete();
  },
  methods: {
    ...mapActions(['getCategory', 'listMenuItem', 'deleteCategory', 'deleteMenuItem']),
    async fetchCategory() {
      try {
        this.category = await this.getCategory(this.categoryUid);
      } catch (error) {
        console.error(error);
        let message = "Error fetching Category!!";
        if(error instanceof HttpNotFound) {
          this.category.notFound = true;
          message = error.data?.detail ?? "Category not found!!";
        } else if(error instanceof HttpServerError) {
          message = this.error.message;
        }
        this.$toast.error(message);
      }
    },
    async fetchMenuItems() {
      try {
        this.menuItemData.loading = true;
        const response = await this.listMenuItem({ category__uid: this.categoryUid, limit: this.limit, offset: this.menuItemData.page++ * this.limit });
        response.results = [...this.menuItemData.results, ...response.results];
        this.menuItemData = { ...this.menuItemData, ...response };
      } catch (err) {
        this.$toast.error("Error fetching Menu Items");
        console.error(err);
      } finally {
        this.menuItemData.loading = false;
      }
    },
    async saveItem() {
      this.menuItemData.results = [];
      this.menuItemData.page = 0;
      await this.fetchMenuItems();
      this.showMenuItemForm = false;
    },
    async saveCategory(v) {
      this.category = v;
      this.showCategoryForm = false;
    },
    startEditing(idx) {
      if(idx === -1) {
        this.instance = {};
      } else {
        this.instance = this.menuItemData.results[idx];
      }
      this.instance.category = this.category;
      this.showMenuItemForm = true;
    },
    async removeCategory() {
      if(!confirm("Are you sure?")) {
        return;
      }
      try {
        this.deleting = true;
        await this.deleteCategory(this.category.uid);
        this.$router.push({ name: 'dashboard-restaurant', params: { uid: this.category.restaurant?.uid } });
      } catch (error) {
        this.$toast.error("Error deleting Category!!");
        console.error(error);
      } finally {
        this.deleting = false;
      }
    },
    async removeItem(item) {
      if(!confirm("Are you sure?")) {
        return;
      }
      try {
        item.deleting = true;
        await this.deleteMenuItem(item.uid);
        this.menuItemData.results = this.menuItemData.results.filter(r => r.uid !== item.uid);
      } catch (error) {
        this.$toast.error("Error deleting Menu Item!!");
        console.error(error);
      } finally {
        item.deleting = false;
      }
    }
  },
};
</script>
