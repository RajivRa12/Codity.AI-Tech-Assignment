import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import api from '../api/axios';
import DataTable from '../components/DataTable';
import FormModal from '../components/FormModal';

export default function Projects() {
  const queryClient = useQueryClient();
  const [isModalOpen, setModalOpen] = useState(false);

  const { data: orgs } = useQuery({ queryKey: ['organizations'], queryFn: async () => (await api.get('projects/organizations/')).data.results });
  
  const { data, isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const res = await api.get('projects/');
      return res.data.results;
    }
  });

  const columns = [
    { header: 'ID', accessor: 'id' },
    { header: 'Name', accessor: 'name' },
    { header: 'Organization', accessor: 'organization' },
    { header: 'Created By', accessor: 'created_by' },
  ];

  const fields = [
    { name: 'name', label: 'Project Name', required: true },
    { name: 'organization', label: 'Organization', type: 'select', required: true, options: orgs?.map(o => ({ value: o.id, label: o.name })) || [] }
  ];

  const handleSubmit = async (formData) => {
    await api.post('projects/', formData);
  };

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Projects</h1>
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
        title="Create Project"
        fields={fields}
        onSubmitAPI={handleSubmit}
        onSuccess={() => queryClient.invalidateQueries(['projects'])}
      />
    </div>
  );
}
