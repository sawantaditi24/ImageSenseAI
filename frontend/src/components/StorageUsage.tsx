import React, { useState, useEffect } from 'react';
import { uploadService } from '../services/api';
import type { StorageUsage } from '../services/api';

const StorageUsageComponent: React.FC = () => {
  const [storageData, setStorageData] = useState<StorageUsage | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStorageUsage();
  }, []);

  const fetchStorageUsage = async () => {
    try {
      setLoading(true);
      const data = await uploadService.getStorageUsage();
      setStorageData(data);
      setError(null);
    } catch (err) {
      setError('Failed to load storage usage');
      console.error('Storage usage error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-2 bg-gray-200 rounded w-full mb-2"></div>
          <div className="h-2 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-red-600 text-sm">{error}</div>
        <button
          onClick={fetchStorageUsage}
          className="mt-2 text-blue-600 hover:text-blue-800 text-sm"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!storageData) {
    return null;
  }

  const { storage_usage, limits } = storageData;
  const usagePercentage = Math.min(storage_usage.usage_percentage, 100);

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Storage Usage</h3>
      
      <div className="space-y-4">
        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Used: {storage_usage.total_size_mb.toFixed(2)} MB</span>
            <span>Limit: {limits.max_storage_mb} MB</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-300 ${
                usagePercentage > 80 ? 'bg-red-500' : 
                usagePercentage > 60 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${usagePercentage}%` }}
            ></div>
          </div>
          <div className="text-xs text-gray-500 mt-1">
            {usagePercentage.toFixed(1)}% used
          </div>
        </div>

        {/* Storage Stats */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {storage_usage.total_files}
            </div>
            <div className="text-sm text-gray-600">Files</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {storage_usage.total_size_gb.toFixed(2)}
            </div>
            <div className="text-sm text-gray-600">GB Used</div>
          </div>
        </div>

        {/* Limits Info */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Storage Limits</h4>
          <div className="space-y-1 text-sm text-gray-600">
            <div>• Maximum file size: {limits.max_file_size_mb} MB</div>
            <div>• Maximum files per user: {limits.max_files}</div>
            <div>• Free tier limit: {storage_usage.free_tier_limit_gb} GB</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StorageUsageComponent; 