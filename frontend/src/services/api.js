import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default {
  getParts() {
    return axios.get(`${API_URL}/parts/`);
  },
  createPart(part) {
    return axios.post(`${API_URL}/parts/`, part);
  },
  getChangeoverTimes() {
    return axios.get(`${API_URL}/changeover-times/`);
  },
  createChangeoverTime(changeoverTime) {
    return axios.post(`${API_URL}/changeover-times/`, changeoverTime);
  },
  exportExcel() {
    return axios.get(`${API_URL}/export-excel/`, { responseType: 'blob' });
  },
  importExcel(formData) {
    return axios.post(`${API_URL}/import-excel/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};