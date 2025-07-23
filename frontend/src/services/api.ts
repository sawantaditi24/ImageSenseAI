import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface UploadResponse {
  message: string;
  data: {
    file_id: string;
    original_url: string;
    thumbnail_url: string;
    original_filename: string;
    upload_date: string;
  };
}

export interface StorageUsage {
  user_id: string;
  storage_usage: {
    total_size_bytes: number;
    total_size_mb: number;
    total_size_gb: number;
    total_files: number;
    free_tier_limit_gb: number;
    usage_percentage: number;
  };
  limits: {
    max_storage_mb: number;
    max_files: number;
    max_file_size_mb: number;
  };
}

export const uploadService = {
  async uploadScreenshot(file: File, userId: string = 'default_user'): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    const response = await api.post<UploadResponse>('/api/v1/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  async deleteScreenshot(fileId: string, userId: string = 'default_user'): Promise<void> {
    await api.delete(`/api/v1/screenshots/${fileId}?user_id=${userId}`);
  },

  async getStorageUsage(userId: string = 'default_user'): Promise<StorageUsage> {
    const response = await api.get<StorageUsage>(`/api/v1/upload/status?user_id=${userId}`);
    return response.data;
  },
};

export default api; 