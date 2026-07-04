import React from 'react';
import clsx from 'clsx';

export default function StatusBadge({ status }) {
  let colorClass = 'bg-gray-100 text-gray-800';
  const lowerStatus = (status || '').toLowerCase();

  switch (lowerStatus) {
    case 'completed':
    case 'online':
    case 'success':
      colorClass = 'bg-green-100 text-green-800';
      break;
    case 'failed':
    case 'offline':
    case 'dead_letter':
    case 'error':
      colorClass = 'bg-red-100 text-red-800';
      break;
    case 'running':
    case 'active':
    case 'claimed':
      colorClass = 'bg-blue-100 text-blue-800';
      break;
    case 'queued':
    case 'delayed':
    case 'scheduled':
    case 'paused':
    case 'pending':
      colorClass = 'bg-yellow-100 text-yellow-800';
      break;
  }

  return (
    <span className={clsx("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize", colorClass)}>
      {lowerStatus.replace('_', ' ')}
    </span>
  );
}
