import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';

export default function Scheduling() {
  const { data, isLoading } = useQuery({
    queryKey: ['schedules'],
    queryFn: async () => {
      const res = await api.get('scheduling/schedules/');
      return res.data.results;
    }
  });

  const columns = [
    { header: 'Name', accessor: 'name' },
    { header: 'Queue', accessor: 'queue' },
    { header: 'Cron', accessor: 'cron_expression' },
    { 
      header: 'Status', 
      cell: (row) => <StatusBadge status={row.is_active ? 'active' : 'paused'} /> 
    },
    { header: 'Next Run', accessor: 'next_run_at' },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Scheduling</h1>
        <button className="bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700">Create</button>
      </div>
      <DataTable columns={columns} data={data} loading={isLoading} />
    </div>
  );
}
