import React from 'react';
import { PackageOpen } from 'lucide-react';

export default function EmptyState({
  title = 'No records found',
  description = 'There are currently no items to display in this section.',
  actionText,
  onAction,
  icon: Icon = PackageOpen,
}) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center bg-gray-50/50 rounded-2xl border border-dashed border-gray-200">
      <div className="w-12 h-12 rounded-2xl bg-white shadow-sm border border-gray-100 flex items-center justify-center text-gray-400 mb-4">
        <Icon className="w-6 h-6" />
      </div>
      <h3 className="text-base font-semibold text-gray-900 mb-1">{title}</h3>
      <p className="text-sm text-gray-500 max-w-sm mb-6 leading-relaxed">{description}</p>
      {actionText && onAction && (
        <button
          onClick={onAction}
          className="px-4 py-2 rounded-lg bg-emerald-600 text-white font-medium text-sm hover:bg-emerald-700 transition shadow-sm"
        >
          {actionText}
        </button>
      )}
    </div>
  );
}

