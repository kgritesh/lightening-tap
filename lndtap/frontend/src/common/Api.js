import axios from "axios";

import Config from "./Config";

export default {
  client: axios.create({
    baseURL: "/api/v1/",
    timeout: Config.API_TIMEOUT,
    headers: {}
  }),

  request(config) {
    return this.client.request(config).then(response => response.data);
  },

  getStats() {
    return this.request({
      url: "/faucet/stats"
    });
  },

  createChannel(channel) {
    return this.request({
      url: "/faucet/open-channel",
      method: "post",
      data: channel
    });
  }
};
