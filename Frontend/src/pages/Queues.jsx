import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import api from '../api/axios';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import FormModal from '../components/FormModal';

export default function Queues() {
  const queryClient = useQueryClient();
  const [isModalOpen, setModalOpen] = useState(false);

  const { data: projects } = useQuery({ queryKey: ['projects'], queryFn: async () => (await api.get('projects/projects/')).data.results });

  const { data, isLoading } = useQuery({
    queryKey: ['queues'],
    queryFn: async () => {
      const res = await api.get('queues/');
      return res.data.results;
    }
  });

  const columns = [
    { header: 'Name', accessor: 'name' },
    { header: 'Project', accessor: 'project' },
    { header: 'Priority', accessor: 'priority' },
    { header: 'Concurrency', accessor: 'concurrency_limit' },
    { 
      header: 'Status', 
      cell: (row) => <StatusBadge status={row.is_paused ? 'paused' : 'active'} /> 
    },
  ];

  const fields = [
    { name: 'name', label: 'Queue Name', required: true },
    { name: 'project', label: 'Project', type: 'select', required: true, options: projects?.map(p => ({ value: p.id, label: p.name })) || [] },
    { name: 'priority', label: 'Priority (higher runs first)', type: 'number', required: true },
    { name: 'concurrency_limit', label: 'Concurrency Limit', type: 'number', required: true }
  ];

  const handleSubmit = async (formData) => {
    await api.post('queues/', {
      ...formData,
      priority: parseInt(formData.priority, 10),
      concurrency_limit: parseInt(formData.concurrency_limit, 10)
    });
  };

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Queues</h1>
        <button 
          onClick={() => setModalOpen(true)}
          className="bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700"
        >
          Create
        </button>
      </div>
      <DataTable columns={columns} data={data} loading={isLoading} />
      
      <FormModal 
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
        title="Create Queue"
        fields={fields}
        onSubmitAPI={handleSubmit}
        onSuccess={() => queryClient.invalidateQueries(['queues'])}
      />
    </div>
  );
}
