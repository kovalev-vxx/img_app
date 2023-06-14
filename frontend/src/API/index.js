import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL

export const API = axios.create({
  baseURL: `${BACKEND_URL}/api/`,
  headers: {
    "Content-Type": "application/json",
  },
});
