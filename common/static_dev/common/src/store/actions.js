import {getRequest, getUrl, deleteRequest } from "./network";
import Types from "./types.js";
import GeneratedActions from './actions.gen.js';

export default {
  async getUser({ commit }) {
    const url = getUrl("user/me");
    const response = await getRequest(url);
    commit(Types.SET_USER, response);
  },

  async deleteRestaurantTable(ctx, uid) {
    const url = getUrl(`restaurant/${uid}/table`);
    return await deleteRequest(url);
  },

  ...GeneratedActions,
};
