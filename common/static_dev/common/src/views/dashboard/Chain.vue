<template>
  <Loader ref="loader">
    <div class="container my-4">
      <PageTitle
        :secondary="`This is where you manage Chain ${user.chain_name}.`"
        primary="Dashboard"/>

      <div class="mb-5">
        <div class="d-flex gap-3 flex-wrap align-items-center mb-4 g-4">
          <div class="flex-grow-1">
            <h6 class="fw-bold mb-0 text-uppercase">
              Restaurants
            </h6>
          </div>

          <Button
            class="btn-primary"
            btn-icon="fas fa-plus"
            @click="() => startEditing(-1)">
            Add Restaurant
          </Button>
        </div>
        <Empty
          v-if="!restaurantData.results?.length"
          title="No Restaurants"
          text="You don't have any Restaurants in your group."
          icon="fas fa-face-frown"/>

        <div v-else>
          <!-- First Table -->
          <div class="table-responsive mb-5">
            <table class="table table-striped align-middle">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Number of Tables</th>
                  <th>Number of Categories</th>
                  <th/>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(restaurant, idx) in restaurantData.results"
                  :key="restaurant.uid">
                  <td>
                    <router-link
                      class="min-w-200"
                      :to="{ name: 'dashboard-restaurant', params: { uid: restaurant.uid } }">
                      {{ restaurant.name }}
                    </router-link>
                  </td>
                  <td>{{ restaurant.table_count }}</td>
                  <td>{{ restaurant.category_count }}</td>
                  <td>
                    <router-link
                      :to="{ name: 'dashboard-order', params: { uid: restaurant.uid } }">
                      <i class="fas me-2 fa-bowl-food "/>
                      Orders
                    </router-link>
                  </td>
                  <td class="text-end">
                    <div>
                      <LoadingButton
                        :is-loading="!!restaurant.deleting"
                        btn-icon="fas fa-pen text-warning"
                        @click="() => startEditing(idx)"/>
                      <LoadingButton
                        :is-loading="!!restaurant.deleting"
                        btn-icon="fas text-danger fa-trash"
                        @click="() => removeRestaurant(restaurant)"/>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <RestaurantFormModal
        v-if="showModal"
        :restaurant="instance"
        @closed="showModal = false"
        @saved="saveRestaurant"/>
    </div>
  </Loader>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Loader from "@/components/Loader.vue";
import Empty from "@/components/Empty.vue";
import PageTitle from "@/components/PageTitle.vue";
import Button from "@/components/Button.vue";
import RestaurantFormModal from "@/components/RestaurantFormModal.vue";
import LoadingButton from "@/components/LoadingButton.vue";

export default {
  name: "Chain",
  components: {
    PageTitle, Empty, Loader, Button, RestaurantFormModal, LoadingButton
  },
  data() {
    return {
      restaurantData: {
        results: [],
        loading: false,
        page: 0,
      },
      showModal: false,
      instance: {}
    };
  },
  computed: {
    ...mapState(['user']),
    limit() {
      return 48;
    }
  },
  async mounted() {
    await this.fetchRestaurant();
    this.$refs.loader.complete();
  },
  methods: {
    ...mapActions(['listRestaurant', 'deleteRestaurant']),
    async fetchRestaurant() {
      try {
        this.restaurantData.loading = true;
        const response = await this.listRestaurant({ limit: this.limit, offset: this.restaurantData.page++ * this.limit });
        response.results = [...this.restaurantData.results, ...response.results];
        this.restaurantData = { ...this.restaurantData, ...response };
      } catch (err) {
        this.$toast.error("Error fetching Restaurants");
        console.error(err);
      } finally {
        this.restaurantData.loading = false;
      }
    },
    startEditing(idx) {
      if(idx === -1) {
        this.instance = {};
      } else {
        this.instance = this.restaurantData.results[idx];
      }
      this.showModal = true;
    },
    async saveRestaurant() {
      this.restaurantData.results = [];
      this.restaurantData.page = 0;
      await this.fetchRestaurant();
      this.showModal = false;
    },
    async removeRestaurant(restaurant) {
      if(!confirm("Are you sure?")) {
        return;
      }
      try {
        restaurant.deleting = true;
        await this.deleteRestaurant(restaurant.uid);
        this.restaurantData.results = this.restaurantData.results.filter(r => r.uid !== restaurant.uid);
      } catch (error) {
        this.$toast.error("Error deleting Restaurant!!");
        console.error(error);
      } finally {
        restaurant.deleting = false;
      }
    },
  },
};
</script>
