import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API, timeout: 90000 });

export const fetchSeasons = () => api.get("/seasons").then((r) => r.data);
export const fetchSeason = (year) => api.get(`/seasons/${year}`).then((r) => r.data);
export const createSimulation = (year, seed) =>
  api.post("/simulate", { year, seed }).then((r) => r.data);
export const fetchSimulation = (id) => api.get(`/simulations/${id}`).then((r) => r.data);
export const runNextRace = (id) => api.post(`/simulations/${id}/next`).then((r) => r.data);
export const finishSimulation = (id) => api.post(`/simulations/${id}/finish`).then((r) => r.data);
export const generateNews = (id) => api.post(`/simulations/${id}/news`).then((r) => r.data);
