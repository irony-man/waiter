<template>
  <div
    id="cart-form"
    class="modal fade"
    tabindex="-1">
    <div class="modal-dialog">
      <Loader ref="loader">
        <form
          method="post"
          class="modal-content"
          @submit.prevent="submitItem">
          <div class="modal-header">
            <h1
              class="modal-title fs-5">
              Customise your item
            </h1>
            <Button
              class="btn-close"
              data-bs-dismiss="modal"/>
          </div>
          <div class="modal-body">
            <div>
              <h2
                class="border-bottom pb-3 mb-4 fw-bold fs-6 text-uppercase">
                {{ item.name }}
              </h2>
            </div>
            <div class="mb-3">
              <Radio
                v-model="instance.price_type"
                name="price_type"
                required
                :choices="choices"/>
            </div>
          </div>
          <div class="modal-footer justify-content-start">
            <LoadingButton
              :is-loading="!!instance.submitting"
              class="btn-primary"
              btn-type="submit">
              Save
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
import Loader from './Loader.vue';
import PageTitle from './PageTitle.vue';
import Radio from './Radio.vue';
import { HttpBadRequestError } from "../store/network";

export default {
  name: "CartFormModal",
  components: { Button, LoadingButton, Loader, PageTitle, Radio },
  props: {
    item: {
      type: Object,
      required: false,
      default: () => { }
    },
  },
  emits: ['closed', 'saved',],
  data() {
    return { modalEl: null, instance: {price_type: 'FULL'}, errors: {} };
  },
  computed: {
    ...mapState(["user"]),
    choices() {
      return [
        {
          value: 'HALF',
          start: 'Half: ',
          end: this.$filters.formatCurrency(this.item.half_price),
        },
        {
          value: 'FULL',
          start: 'Full: ',
          end: this.$filters.formatCurrency(this.item.full_price),
        }
      ];
    }
  },
  mounted() {
    this.$refs.loader.complete();
    this.modalEl = document.getElementById('cart-form');
    this.modal = new window.bootstrap.Modal(this.modalEl, { backdrop: 'static', keyboard: true });
    this.modalEl.addEventListener('hidden.bs.modal', () => this.$emit('closed'));
    if (this.modal) {
      this.modal.show();
    }
    this.instance = { ...this.instance, ...this.item };
  },
  beforeUnmount() {
    if (this.modal) {
      this.modal.hide();
    }
  },
  methods: {
    ...mapActions(['listRestaurant', 'createCategory', 'updateCategory']),
    async submitItem() {
      try {
        this.instance.submitting = true;
        this.$emit('saved', {
          uid: this.instance.uid,
          name: this.instance.name,
          price: this.instance.price_type === 'FULL' ? this.instance.full_price:this.instance.half_price,
          type: this.instance.price_type,
        });
      } catch (error) {
        if (error instanceof HttpBadRequestError) {
          this.errors = error.data;
        }
        this.$toast.error("Error saving Item!!");
        console.error(error);
      } finally {
        this.instance.submitting = false;
      }
    }
  }
};
</script>
