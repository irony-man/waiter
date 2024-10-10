import {getRequest, getUrl, deleteRequest } from "./network";
import Types from "./types.js";
import GeneratedActions from './actions.gen.js';

export default {
  async getUser({ commit }) {
    const url = getUrl("user/me");
    const response = await getRequest(url);
    commit(Types.SET_USER, response);
    return response;
  },

  setCart({ commit }, cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    commit(Types.SET_CART, cart);
  },

  async deleteRestaurantTable(ctx, uid) {
    const url = getUrl(`restaurant/${uid}/table`);
    return await deleteRequest(url);
  },

  async getTableQRCode(ctx, {uid, query}) {
    const url = `/table-qr-code/${uid}/`;
    return await getRequest(url, query);
  },

  async getCart(ctx, uid) {
    const response =  await getRequest(`/table-qr-code/${uid}/`, {cart: localStorage.getItem('cart') || '{}'});
    ctx.commit(Types.SET_CART, response.cart);
    return response;
  },

  ...GeneratedActions,
};
