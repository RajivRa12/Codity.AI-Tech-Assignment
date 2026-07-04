import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoutes from './routes/ProtectedRoutes';
import MainLayout from './layouts/MainLayout';
import Login from './pages/Login';
import Register from './pages/Register';

const queryClient = new QueryClient();

import Dashboard from './pages/Dashboard';
import Organizations from './pages/Organizations';
import Projects from './pages/Projects';
import Queues from './pages/Queues';
import Jobs from './pages/Jobs';
import Workers from './pages/Workers';
import Scheduling from './pages/Scheduling';
import RetryPolicies from './pages/RetryPolicies';
import Logs from './pages/Logs';

// Placeholder components for pages we haven't built yet
const Profile = () => <div className="p-4">User Profile (Coming Soon)</div>;
const NotFound = () => <div className="p-4">404 - Not Found</div>;

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            <Route element={<ProtectedRoutes />}>
              <Route element={<MainLayout />}>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/organizations" element={<Organizations />} />
                <Route path="/projects" element={<Projects />} />
                <Route path="/queues" element={<Queues />} />
                <Route path="/jobs" element={<Jobs />} />
                <Route path="/workers" element={<Workers />} />
                <Route path="/scheduling" element={<Scheduling />} />
                <Route path="/retry-policies" element={<RetryPolicies />} />
                <Route path="/logs" element={<Logs />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="*" element={<NotFound />} />
              </Route>
            </Route>
          </Routes>
        </BrowserRouter>
        <Toaster position="top-right" />
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
