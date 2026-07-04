import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import api from '../api/axios';
import DataTable from '../components/DataTable';
import FormModal from '../components/FormModal';

export default function Organizations() {
  const queryClient = useQueryClient();
  const [isModalOpen, setModalOpen] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ['organizations'],
    queryFn: async () => {
      const res = await api.get('projects/organizations/');
      return res.data.results;
    }
  });

  const columns = [
    { header: 'ID', accessor: 'id' },
    { header: 'Name', accessor: 'name' },
    { header: 'Owner', accessor: 'owner' },
  ];

  const fields = [
    { name: 'name', label: 'Organization Name', required: true }
  ];

  const handleSubmit = async (formData) => {
    await api.post('projects/organizations/', formData);
  };

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Organizations</h1>
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
        title="Create Organization"
        fields={fields}
        onSubmitAPI={handleSubmit}
        onSuccess={() => queryClient.invalidateQueries(['organizations'])}
      />
    </div>
  );
}
