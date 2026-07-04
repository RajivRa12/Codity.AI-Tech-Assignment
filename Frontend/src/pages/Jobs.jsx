import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';

export default function Jobs() {
  const { data, isLoading } = useQuery({
    queryKey: ['jobs'],
    queryFn: async () => {
      const res = await api.get('jobs/');
      return res.data.results;
    }
  });

  const columns = [
    { header: 'ID', accessor: 'id' },
    { header: 'Queue', accessor: 'queue' },
    { header: 'Type', accessor: 'job_type' },
    { 
      header: 'Status', 
      cell: (row) => <StatusBadge status={row.status} /> 
    },
    { header: 'Scheduled At', accessor: 'scheduled_at' },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Jobs</h1>
        <button className="bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700">Create</button>
      </div>
      <DataTable columns={columns} data={data} loading={isLoading} />
    </div>
  );
}
