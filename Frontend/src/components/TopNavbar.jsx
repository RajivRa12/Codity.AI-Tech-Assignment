import React from 'react';
import { useAuth } from '../context/AuthContext';
import { UserCircleIcon, ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';

export default function TopNavbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="sticky top-0 z-10 flex h-16 flex-shrink-0 bg-white shadow-sm border-b border-gray-200">
      <div className="flex flex-1 justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex flex-1">
          {/* Breadcrumbs or search can go here */}
        </div>
        <div className="ml-4 flex items-center md:ml-6 gap-4">
          <div className="flex items-center gap-2 text-sm text-gray-700 font-medium cursor-pointer" onClick={() => navigate('/profile')}>
            <UserCircleIcon className="h-6 w-6 text-gray-400" />
            <span>{user?.username || 'User'}</span>
          </div>
          <button
            onClick={handleLogout}
            className="rounded-md bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none transition-colors flex items-center gap-1 text-sm"
          >
            <ArrowRightOnRectangleIcon className="h-5 w-5" aria-hidden="true" />
            <span className="sr-only sm:not-sr-only">Logout</span>
          </button>
        </div>
      </div>
    </div>
  );
}
