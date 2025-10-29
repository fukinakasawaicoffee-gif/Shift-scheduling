import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// リクエストインターセプター（トークンを自動付与）
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// レスポンスインターセプター（エラーハンドリング）
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// 認証API
export const authAPI = {
  login: (username: string, password: string) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  register: (data: any) => api.post('/auth/register', data),
};

// 部署API
export const departmentAPI = {
  getAll: () => api.get('/departments/'),
  getById: (id: number) => api.get(`/departments/${id}`),
  create: (data: any) => api.post('/departments/', data),
  update: (id: number, data: any) => api.put(`/departments/${id}`, data),
  delete: (id: number) => api.delete(`/departments/${id}`),
};

// 従業員API
export const employeeAPI = {
  getAll: (departmentId?: number) =>
    api.get('/employees/', { params: { department_id: departmentId } }),
  getById: (id: number) => api.get(`/employees/${id}`),
  create: (data: any) => api.post('/employees/', data),
  update: (id: number, data: any) => api.put(`/employees/${id}`, data),
  delete: (id: number) => api.delete(`/employees/${id}`),
};

// シフトパターンAPI
export const shiftPatternAPI = {
  getAll: (departmentId?: number) =>
    api.get('/shift-patterns/', { params: { department_id: departmentId } }),
  getById: (id: number) => api.get(`/shift-patterns/${id}`),
  create: (data: any) => api.post('/shift-patterns/', data),
  update: (id: number, data: any) => api.put(`/shift-patterns/${id}`, data),
  delete: (id: number) => api.delete(`/shift-patterns/${id}`),
};

// シフト必要人数API
export const shiftRequirementAPI = {
  getAll: (params?: {
    department_id?: number;
    start_date?: string;
    end_date?: string;
  }) => api.get('/shift-requirements/', { params }),
  getById: (id: number) => api.get(`/shift-requirements/${id}`),
  create: (data: any) => api.post('/shift-requirements/', data),
  update: (id: number, data: any) => api.put(`/shift-requirements/${id}`, data),
  delete: (id: number) => api.delete(`/shift-requirements/${id}`),
};

// スケジュールAPI
export const scheduleAPI = {
  getAll: (params?: {
    department_id?: number;
    employee_id?: number;
    start_date?: string;
    end_date?: string;
  }) => api.get('/schedules/', { params }),
  getById: (id: number) => api.get(`/schedules/${id}`),
  create: (data: any) => api.post('/schedules/', data),
  update: (id: number, data: any) => api.put(`/schedules/${id}`, data),
  delete: (id: number) => api.delete(`/schedules/${id}`),
  generate: (data: any) => api.post('/schedules/generate', data),
};

// 休暇申請API
export const leaveRequestAPI = {
  getAll: (params?: { employee_id?: number; status?: string }) =>
    api.get('/leave-requests/', { params }),
  getById: (id: number) => api.get(`/leave-requests/${id}`),
  create: (data: any) => api.post('/leave-requests/', data),
  update: (id: number, data: any) => api.put(`/leave-requests/${id}`, data),
  delete: (id: number) => api.delete(`/leave-requests/${id}`),
  approve: (id: number) => api.post(`/leave-requests/${id}/approve`),
  reject: (id: number) => api.post(`/leave-requests/${id}/reject`),
};
