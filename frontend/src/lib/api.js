import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API, timeout: 90000 });

export const fetchSeasons = () => api.get("/seasons").then((r) => r.data);
export const fetchSeason = (year) => api.get(`/seasons/${year}`).then((r) => r.data);
export const createSimulation = (year, seed, realityId) =>
  api.post("/simulate", { year, seed, reality_id: realityId }).then((r) => r.data);
export const fetchSimulation = (id) => api.get(`/simulations/${id}`).then((r) => r.data);
export const runNextRace = (id) => api.post(`/simulations/${id}/next`).then((r) => r.data);
export const finishSimulation = (id, fast = false) =>
  api.post(`/simulations/${id}/finish${fast ? "?fast=true" : ""}`).then((r) => r.data);
export const generateNews = (id) => api.post(`/simulations/${id}/news`).then((r) => r.data);

// Minha Realidade
export const createReality = (name) => api.post("/realities", { name }).then((r) => r.data);
export const listRealities = () => api.get("/realities").then((r) => r.data);
export const fetchReality = (id) => api.get(`/realities/${id}`).then((r) => r.data);
export const commitSeason = (rid, simId) =>
  api.post(`/realities/${rid}/commit/${simId}`).then((r) => r.data);
export const resolveEvent = (rid, year, choiceId) =>
  api.post(`/realities/${rid}/resolve`, { year, choice_id: choiceId }).then((r) => r.data);
