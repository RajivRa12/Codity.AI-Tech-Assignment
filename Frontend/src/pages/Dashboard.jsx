import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, LineChart, Line, ResponsiveContainer } from 'recharts';
import api from '../api/axios';
import { 
  BuildingOfficeIcon, 
  FolderIcon, 
  QueueListIcon, 
  BriefcaseIcon, 
  CpuChipIcon, 
  CalendarDaysIcon, 
  ArrowPathIcon,
  DocumentTextIcon 
} from '@heroicons/react/24/outline';

const fetchCount = async (endpoint) => {
  const { data } = await api.get(`${endpoint}?limit=1`);
  return data.count;
};

const fetchJobs = async () => {
  const { data } = await api.get('jobs/?limit=100');
  return data.results;
};

const fetchWorkers = async () => {
  const { data } = await api.get('workers/?limit=100');
  return data.results;
};

const fetchQueues = async () => {
  const { data } = await api.get('queues/?limit=100');
  return data.results;
};

const COLORS = ['#3b82f6', '#10b981', '#ef4444', '#f59e0b', '#6366f1'];

export default function Dashboard() {
  const { data: orgCount = 0 } = useQuery({ queryKey: ['orgsCount'], queryFn: () => fetchCount('projects/organizations/') });
  const { data: projCount = 0 } = useQuery({ queryKey: ['projCount'], queryFn: () => fetchCount('projects/projects/') });
  const { data: queueCount = 0 } = useQuery({ queryKey: ['queueCount'], queryFn: () => fetchCount('queues/') });
  const { data: jobCount = 0 } = useQuery({ queryKey: ['jobCount'], queryFn: () => fetchCount('jobs/') });
  const { data: workerCount = 0 } = useQuery({ queryKey: ['workerCount'], queryFn: () => fetchCount('workers/') });
  const { data: scheduleCount = 0 } = useQuery({ queryKey: ['scheduleCount'], queryFn: () => fetchCount('scheduling/schedules/') });
  const { data: retryCount = 0 } = useQuery({ queryKey: ['retryCount'], queryFn: () => fetchCount('retry/policies/') });
  const { data: logCount = 0 } = useQuery({ queryKey: ['logCount'], queryFn: () => fetchCount('logs/') });

  const { data: jobs = [] } = useQuery({ queryKey: ['dashboardJobs'], queryFn: fetchJobs });
  const { data: workers = [] } = useQuery({ queryKey: ['dashboardWorkers'], queryFn: fetchWorkers });
  const { data: queues = [] } = useQuery({ queryKey: ['dashboardQueues'], queryFn: fetchQueues });

  const stats = [
    { name: 'Organizations', stat: orgCount, icon: BuildingOfficeIcon },
    { name: 'Projects', stat: projCount, icon: FolderIcon },
    { name: 'Queues', stat: queueCount, icon: QueueListIcon },
    { name: 'Jobs', stat: jobCount, icon: BriefcaseIcon },
    { name: 'Workers', stat: workerCount, icon: CpuChipIcon },
    { name: 'Schedules', stat: scheduleCount, icon: CalendarDaysIcon },
    { name: 'Retry Policies', stat: retryCount, icon: ArrowPathIcon },
    { name: 'Logs', stat: logCount, icon: DocumentTextIcon },
  ];

  // Aggregations for Charts
  const jobStatusCounts = jobs.reduce((acc, job) => {
    acc[job.status] = (acc[job.status] || 0) + 1;
    return acc;
  }, {});
  const jobPieData = Object.keys(jobStatusCounts).map(key => ({ name: key, value: jobStatusCounts[key] }));

  const workerStatusCounts = workers.reduce((acc, worker) => {
    acc[worker.status] = (acc[worker.status] || 0) + 1;
    return acc;
  }, {});
  const workerPieData = Object.keys(workerStatusCounts).map(key => ({ name: key, value: workerStatusCounts[key] }));

  const queueBarData = queues.map(q => ({ name: q.name, Priority: q.priority, Concurrency: q.concurrency_limit }));

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
      
      {/* Metric Cards */}
      <dl className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => (
          <div key={item.name} className="relative overflow-hidden rounded-lg bg-white px-4 pt-5 pb-12 shadow sm:px-6 sm:pt-6">
            <dt>
              <div className="absolute rounded-md bg-primary-500 p-3">
                <item.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">{item.name}</p>
            </dt>
            <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
              <p className="text-2xl font-semibold text-gray-900">{item.stat}</p>
            </dd>
          </div>
        ))}
      </dl>

      {/* Charts */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        
        {/* Job Status Pie Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Job Status Distribution</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={jobPieData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value" label>
                  {jobPieData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                </Pie>
                <RechartsTooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Worker Status Donut Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Worker Status</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={workerPieData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value" label>
                  {workerPieData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                </Pie>
                <RechartsTooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Queue Statistics Bar Chart */}
        <div className="bg-white rounded-lg shadow p-6 lg:col-span-2">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Queue Statistics</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={queueBarData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Bar dataKey="Concurrency" fill="#3b82f6" />
                <Bar dataKey="Priority" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
