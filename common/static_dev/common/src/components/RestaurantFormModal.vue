<template>
  <div
    id="restaurant-form"
    class="modal fade"
    tabindex="-1">
    <div class="modal-dialog">
      <Loader ref="loader">
        <form
          method="post"
          class="modal-content"
          @submit.prevent="submitRestaurant">
          <div class="modal-header">
            <h1
              class="modal-title fs-5">
              Restaurant Form
            </h1>
            <Button
              class="btn-close"
              data-bs-dismiss="modal"/>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <Input
                v-model="instance.name"
                label="Name"
                name="name"
                required
                :error="errors.name"/>
            </div>
            <div class="mb-3">
              <Input
                v-model="user.chain_name"
                label="Chain"
                name="chain"
                disabled
                :error="errors.chain"/>
            </div>
          </div>
          <div class="modal-footer justify-content-start">
            <LoadingButton
              :is-loading="!!instance.submitting"
              class="btn-primary"
              btn-type="submit">
              Save Restaurant
            </LoadingButton>
            <LoadingButton
              :is-loading="!!instance.submitting"
              class="btn-secondary"
              data-bs-dismiss="modal">
              Close
            </LoadingButton>
          </div>
        </form>
      </Loader>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Button from './Button.vue';
import LoadingButton from './LoadingButton.vue';
import Input from './Input.vue';
import Loader from './Loader.vue';
import { HttpBadRequestError } from "../store/network";

export default {
  name: "RestaurantFormModal",
  components: { Input, Button, LoadingButton, Loader },
  props: {
    restaurant: {
      type: Object,
      required: false,
      default: () => { }
    },
  },
  emits: ['closed', 'saved',],
  data() {
    return { modalEl: null, instance: {}, errors: {} };
  },
  computed: {
    ...mapState(["user"]),
  },
  mounted() {
    this.$refs.loader.complete();
    this.modalEl = document.getElementById('restaurant-form');
    this.modal = new window.bootstrap.Modal(this.modalEl, { backdrop: 'static', keyboard: true });
    this.modalEl.addEventListener('hidden.bs.modal', () => this.$emit('closed'));
    if (this.modal) {
      this.modal.show();
    }
    this.instance = { ...this.instance, ...this.restaurant };
  },
  beforeUnmount() {
    if (this.modal) {
      this.modal.hide();
    }
  },
  methods: {
    ...mapActions(['createRestaurant', 'updateRestaurant']),
    async submitRestaurant() {
      try {
        this.instance.submitting = true;
        if (this.instance.uid) {
          this.instance = await this.updateRestaurant({ uid: this.instance.uid, formData: this.instance });
        } else {
          this.instance = await this.createRestaurant(this.instance);
        }
        this.$toast.success("Restaurant saved!!");
        this.$emit('saved', this.instance);
      } catch (error) {
        if (error instanceof HttpBadRequestError) {
          this.errors = error.data;
        }
        this.$toast.error("Error saving Restaurant!!");
        console.error(error);
      } finally {
        this.instance.submitting = false;
      }
    }
  }
};
</script>
