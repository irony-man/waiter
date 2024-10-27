

export default {
  orderWebsocket(ctx, uid) {
    const connection = new WebSocket(`/ws/order/${uid}/`);

    connection.onopen = () => {
      console.log('WebSocket connected');
    };

    connection.onclose = () => {
      console.log('WebSocket closed');
    };

    // this.connection.onmessage = this.updateOrder;
    return connection;
  }
};
