import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';

export default function Logs() {
  const { data, isLoading } = useQuery({
    queryKey: ['logs'],
    queryFn: async () => {
      const res = await api.get('logs/');
      return res.data.results;
    }
  });

  const columns = [
    { header: 'Timestamp', accessor: 'created_at' },
    { 
      header: 'Level', 
      cell: (row) => <StatusBadge status={row.level === 'ERROR' ? 'failed' : row.level === 'WARNING' ? 'paused' : 'success'} /> 
    },
    { header: 'Event', accessor: 'event_type' },
    { header: 'Message', accessor: 'message' },
  ];

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">System Logs</h1>
      </div>
      <DataTable columns={columns} data={data} loading={isLoading} />
    </div>
  );
}
