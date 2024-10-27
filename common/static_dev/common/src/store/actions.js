import { getRequest, getUrl, deleteRequest, postRequest } from "./network";
import Types from "./types.js";
import GeneratedActions from "./actions.gen.js";
import cookiesLib from "../cookiesLib.js";
import webSocket from "./webSocket.js";

export default {
  async getUser({ commit }) {
    const url = getUrl("user/me");
    const response = await getRequest(url);
    commit(Types.SET_USER, response);
    return response;
  },

  addCartItem({ commit, state }, item) {
    const { cart } = state;
    const {price_type} = item;
    const price = price_type === "FULL" ? item.full_price : item.half_price;
    const key = `${item.uid}/${price_type}`;
    let quantity = (key in cart ? cart[key].quantity : 0) + 1;
    cart[key] = { price, quantity, price_type, menu_item: item };

    cookiesLib.setCookie("cart", JSON.stringify(cart));
    commit(Types.SET_CART, cart);
  },

  removeCartItem({ commit, state }, {item, priceTypes= ['HALF', 'FULL']}) {
    const { cart } = state;
    for (const type of priceTypes) {
      const key = `${item.uid}/${type}`;
      if (key in cart) {
        const quantity = Math.max(--cart[key].quantity, 0);
        if(quantity === 0) {
          delete cart[key];
        }
        break;
      }
    }
    cookiesLib.setCookie("cart", JSON.stringify(cart));
    commit(Types.SET_CART, cart);
  },

  setCart({ commit }, cart) {
    cookiesLib.setCookie("cart", JSON.stringify(cart));
    commit(Types.SET_CART, cart);
  },

  async deleteRestaurantTable(ctx, uid) {
    const url = getUrl(`restaurant/${uid}/table`);
    return await deleteRequest(url);
  },

  async getCart(ctx, uid) {
    const url = getUrl(`table/${uid}/cart`);
    const response = await getRequest(url);
    ctx.commit(Types.SET_CART, response.cart);
    return response;
  },

  async getTableCategory(ctx, uid) {
    const url = getUrl(`table/${uid}/categories`);
    return await getRequest(url);
  },

  async getTableOrder(ctx, uid) {
    return await getRequest(`/order/${uid}/`);
  },

  async createTableOrder(ctx, uid) {
    return await postRequest(`/order/${uid}/`);
  },

  ...GeneratedActions,
  ...webSocket,
};
