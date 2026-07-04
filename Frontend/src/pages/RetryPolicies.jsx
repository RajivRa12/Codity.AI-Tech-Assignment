import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';
import DataTable from '../components/DataTable';

export default function RetryPolicies() {
  const { data, isLoading } = useQuery({
    queryKey: ['retryPolicies'],
    queryFn: async () => {
      const res = await api.get('retry/policies/');
      return res.data.results;
    }
  });

  const columns = [
    { header: 'Name', accessor: 'name' },
    { header: 'Type', accessor: 'policy_type' },
    { header: 'Max Retries', accessor: 'max_retries' },
    { header: 'Initial Delay', accessor: 'initial_delay_seconds' },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Retry Policies</h1>
        <button className="bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700">Create</button>
      </div>
      <DataTable columns={columns} data={data} loading={isLoading} />
    </div>
  );
}
