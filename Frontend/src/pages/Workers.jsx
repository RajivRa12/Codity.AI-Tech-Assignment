import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';

export default function Workers() {
  const { data, isLoading } = useQuery({
    queryKey: ['workers'],
    queryFn: async () => {
      const res = await api.get('workers/');
      return res.data.results;
    }
  });

  const columns = [
    { header: 'Name', accessor: 'name' },
    { header: 'Hostname', accessor: 'hostname' },
    { header: 'Concurrency', accessor: 'concurrency' },
    { 
      header: 'Status', 
      cell: (row) => <StatusBadge status={row.status} /> 
    },
    { header: 'Last Heartbeat', accessor: 'last_heartbeat' },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Workers</h1>
      </div>
      <DataTable columns={columns} data={data} loading={isLoading} />
    </div>
  );
}
