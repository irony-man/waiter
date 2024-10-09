import { createStore } from "vuex";
import actions from "./actions";
import mutations from "./mutations";

const state = {
  user: {},
  cart: {}
};

const store = createStore({
  state: state,
  actions: actions,
  mutations: mutations,
});

export default store;
