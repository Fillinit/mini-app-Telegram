import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

export const getProducts = async () => {
  const res = await axios.get(`${API_URL}/products/`);
  return res.data;
};

export const createOrder = async (order) => {
  const res = await axios.post(`${API_URL}/orders/`, order);
  return res.data;
};

export const sendInvoice = async (orderId) => {
  const res = await axios.post(`${API_URL}/orders/${orderId}/send_invoice/`);
  return res.data;
};
