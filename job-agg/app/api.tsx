import axios from "axios";

const api = axios.create({
    baseURL: "https://job-aggregator-kohl.vercel.app/"
});

export default api;