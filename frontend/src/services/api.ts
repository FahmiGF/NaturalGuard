import axios from 'axios';
import { DisasterEvent, DisasterAlert } from '../types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = {
  async getDisasters(hazard?: string): Promise<DisasterEvent[]> {
    const params = hazard ? { hazard } : {};
    const res = await axios.get(`${API_BASE}/disasters`, { params });
    return res.data;
  },

  async getAlerts(isOfficial?: boolean): Promise<DisasterAlert[]> {
    const params: any = {};
    if (isOfficial !== undefined) params.is_official = isOfficial;
    const res = await axios.get(`${API_BASE}/alerts`, { params });
    return res.data;
  },

  async getForecasts(hazard?: string) {
    const params = hazard ? { hazard } : {};
    const res = await axios.get(`${API_BASE}/forecast`, { params });
    return res.data;
  },

  async askCopilot(question: string) {
    const res = await axios.post(`${API_BASE}/copilot/chat`, { question });
    return res.data;
  },

  async getVoiceScript(alertId?: string) {
    const params = alertId ? { alert_id: alertId } : {};
    const res = await axios.get(`${API_BASE}/copilot/voice-script`, { params });
    return res.data;
  },

  async getDataSources() {
    const res = await axios.get(`${API_BASE}/data-sources`);
    return res.data;
  },

  async getEvaluationMetrics() {
    const res = await axios.get(`${API_BASE}/evaluation/metrics`);
    return res.data;
  }
};
