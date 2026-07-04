import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  HomeIcon, 
  BuildingOfficeIcon, 
  FolderIcon, 
  QueueListIcon, 
  BriefcaseIcon, 
  CpuChipIcon, 
  CalendarDaysIcon, 
  ArrowPathIcon,
  DocumentTextIcon 
} from '@heroicons/react/24/outline';
import clsx from 'clsx';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Organizations', href: '/organizations', icon: BuildingOfficeIcon },
  { name: 'Projects', href: '/projects', icon: FolderIcon },
  { name: 'Queues', href: '/queues', icon: QueueListIcon },
  { name: 'Jobs', href: '/jobs', icon: BriefcaseIcon },
  { name: 'Workers', href: '/workers', icon: CpuChipIcon },
  { name: 'Scheduling', href: '/scheduling', icon: CalendarDaysIcon },
  { name: 'Retry Policies', href: '/retry-policies', icon: ArrowPathIcon },
  { name: 'Logs', href: '/logs', icon: DocumentTextIcon },
];

export default function Sidebar() {
  return (
    <div className="flex flex-col w-64 border-r border-gray-200 bg-white">
      <div className="flex h-16 shrink-0 items-center px-6">
        <h1 className="text-xl font-bold text-primary-600">Scheduler</h1>
      </div>
      <div className="flex flex-1 flex-col overflow-y-auto">
        <nav className="flex-1 space-y-1 px-4 py-4">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                clsx(
                  isActive
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-primary-600',
                  'group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors'
                )
              }
            >
              {({ isActive }) => (
                <>
                  <item.icon
                    className={clsx(
                      isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-primary-600',
                      'mr-3 h-5 w-5 flex-shrink-0 transition-colors'
                    )}
                    aria-hidden="true"
                  />
                  {item.name}
                </>
              )}
            </NavLink>
          ))}
        </nav>
      </div>
    </div>
  );
}
