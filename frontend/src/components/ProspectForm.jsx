import React, { useState } from 'react';
import { Search, UserPlus, Building2, Mail, Sparkles, Loader2 } from 'lucide-react';

export default function ProspectForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    company_name: '',
    industry: 'SaaS',
    contact_name: '',
    contact_title: '',
    icp_criteria: {},
    notes: '',
  });

  const industries = [
    'SaaS', 'FinTech', 'HealthTech', 'EdTech', 'MarTech',
    'HR Tech', 'Cybersecurity', 'E-commerce', 'AI/ML', 'DevOps'
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.company_name.trim()) return;
    onSubmit(formData);
  };

  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-5">
        <div className="p-2.5 rounded-xl bg-primary-500/10">
          <Search className="w-5 h-5 text-primary-400" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-white">Prospecting Agent</h3>
          <p className="text-xs text-surface-200/50">AI-powered lead scoring & outreach generation</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-surface-200/60 mb-1.5">
              <Building2 className="w-3.5 h-3.5 inline mr-1" />
              Company Name *
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g., TechFlow Inc"
              value={formData.company_name}
              onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
              required
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-surface-200/60 mb-1.5">
              Industry
            </label>
            <select
              className="input-field"
              value={formData.industry}
              onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
            >
              {industries.map(i => (
                <option key={i} value={i}>{i}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-surface-200/60 mb-1.5">
              <UserPlus className="w-3.5 h-3.5 inline mr-1" />
              Contact Name
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g., Sarah Johnson"
              value={formData.contact_name}
              onChange={(e) => setFormData({ ...formData, contact_name: e.target.value })}
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-surface-200/60 mb-1.5">
              Contact Title
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g., VP of Sales"
              value={formData.contact_title}
              onChange={(e) => setFormData({ ...formData, contact_title: e.target.value })}
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-medium text-surface-200/60 mb-1.5">
            Notes (optional)
          </label>
          <textarea
            className="input-field min-h-[60px] resize-none"
            placeholder="Any additional context about the prospect..."
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
          />
        </div>

        <button
          type="submit"
          disabled={isLoading || !formData.company_name.trim()}
          className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Analyzing Prospect...
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              Run Prospecting Agent
            </>
          )}
        </button>
      </form>
    </div>
  );
}
