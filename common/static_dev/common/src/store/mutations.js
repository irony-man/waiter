import Types from "./types";

export default {
  [Types.SET_USER](state, data) {
    state.user = data;
  },
  [Types.SET_CART](state, data) {
    state.cart = data;
  },
};
