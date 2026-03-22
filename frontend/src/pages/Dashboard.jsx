import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { Search, Download, ArrowRight, User, Upload, Briefcase, RefreshCw } from 'lucide-react';
import { motion } from 'framer-motion';

const Dashboard = () => {
  const [candidates, setCandidates] = useState([]);
  const [jobTitle, setJobTitle] = useState('');
  const [jobId, setJobId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  const fetchData = async () => {
    setLoading(true);
    try {
      // Auto-load the first available job
      const jobsRes = await api.listJobs();
      const jobs = jobsRes.data.data;
      if (!jobs || jobs.length === 0) {
        setLoading(false);
        return;
      }
      const firstJob = jobs[0];
      setJobId(firstJob.job_id);
      setJobTitle(firstJob.title);

      // Fetch rankings
      const rankRes = await api.getRankings(firstJob.job_id);
      setCandidates(rankRes.data.data || []);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  const getRowStyle = (score) => {
    if (score > 75) return 'border-l-4 border-emerald-500/50';
    if (score > 50) return 'border-l-4 border-amber-500/50';
    return 'border-l-4 border-rose-500/50';
  };

  const getScoreBadge = (score) => {
    if (score > 75) return 'bg-emerald-500/15 text-emerald-400 ring-1 ring-emerald-500/30';
    if (score > 50) return 'bg-amber-500/15 text-amber-400 ring-1 ring-amber-500/30';
    return 'bg-rose-500/15 text-rose-400 ring-1 ring-rose-500/30';
  };

  const filtered = candidates.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.top_skill_gap.toLowerCase().includes(search.toLowerCase())
  );

  const top = candidates[0]?.score ?? 0;
  const avg = candidates.length
    ? Math.round(candidates.reduce((s, c) => s + c.score, 0) / candidates.length)
    : 0;

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 font-sans">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-[#020617]/80 backdrop-blur-xl border-b border-white/5 px-8 py-5 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-cyan-500 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <Briefcase size={20} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
              SmartHire AI
            </h1>
            <p className="text-xs text-slate-500 font-medium">Resume × Job Intelligence</p>
          </div>
        </div>
        <div className="flex gap-3">
          <button
            onClick={fetchData}
            className="p-2.5 bg-slate-900 border border-white/10 rounded-xl text-slate-400 hover:text-white transition-colors"
          >
            <RefreshCw size={16} />
          </button>
          <button
            onClick={() => navigate('/upload')}
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-semibold shadow-lg shadow-indigo-500/20 transition-all flex items-center gap-2 text-sm"
          >
            <Upload size={16} /> Upload Resumes
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-8 py-10">
        {/* Active Job Banner */}
        {jobTitle && (
          <motion.div
            initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
            className="mb-8 p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-2xl flex items-center gap-3"
          >
            <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
            <span className="text-sm font-semibold text-indigo-300">Active Job Role:</span>
            <span className="text-sm text-slate-300">{jobTitle}</span>
          </motion.div>
        )}

        {/* Stats */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-10">
          {[
            { label: 'Total Candidates', value: candidates.length, color: 'text-white' },
            { label: 'Top Match Score', value: `${top}%`, color: 'text-emerald-400' },
            { label: 'Average Score', value: `${avg}%`, color: 'text-indigo-400' },
          ].map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="p-6 bg-slate-900/60 border border-white/5 rounded-2xl"
            >
              <p className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-3">{stat.label}</p>
              <p className={`text-4xl font-extrabold tracking-tight ${stat.color}`}>{stat.value}</p>
            </motion.div>
          ))}
        </section>

        {/* Search */}
        <div className="flex justify-between items-center mb-6">
          <div className="relative w-80">
            <Search className="absolute left-4 top-3.5 text-slate-500" size={16} />
            <input
              type="text"
              placeholder="Search candidates or skills..."
              className="w-full bg-slate-900/50 border border-white/10 rounded-xl py-3 pl-11 pr-4 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none placeholder:text-slate-600"
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-3 bg-slate-900 border border-white/10 rounded-xl text-sm text-slate-400 hover:text-white transition-colors">
            <Download size={16} /> Export
          </button>
        </div>

        {/* Table */}
        <div className="bg-slate-900/40 backdrop-blur-xl border border-white/5 rounded-3xl overflow-hidden shadow-2xl">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-white/5 text-slate-500 text-[11px] font-bold uppercase tracking-widest">
                <th className="px-7 py-5">#</th>
                <th className="px-7 py-5">Candidate</th>
                <th className="px-7 py-5">Match Score</th>
                <th className="px-7 py-5">Key Gap</th>
                <th className="px-7 py-5">Status</th>
                <th className="px-7 py-5 text-right">View</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.04]">
              {loading ? (
                <tr>
                  <td colSpan="6" className="py-24 text-center text-slate-500">
                    <div className="flex flex-col items-center gap-4">
                      <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
                      <span className="text-sm">Loading intelligence data...</span>
                    </div>
                  </td>
                </tr>
              ) : filtered.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-24 text-center">
                    <div className="flex flex-col items-center gap-4 text-slate-500">
                      <User size={40} className="opacity-20" />
                      <p className="text-sm">No candidates yet. <button onClick={() => navigate('/upload')} className="text-indigo-400 underline">Upload resumes</button> to get started.</p>
                    </div>
                  </td>
                </tr>
              ) : (
                filtered.map((c, i) => (
                  <motion.tr
                    key={c.candidate_id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                    onClick={() => navigate(`/candidate/${c.candidate_id}`)}
                    className={`group cursor-pointer hover:bg-white/[0.025] transition-all ${getRowStyle(c.score)}`}
                  >
                    <td className="px-7 py-5 text-slate-600 font-bold text-sm">{i + 1}</td>
                    <td className="px-7 py-5">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 bg-gradient-to-br from-slate-700 to-slate-800 rounded-xl flex items-center justify-center text-slate-400 text-xs font-bold">
                          {c.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
                        </div>
                        <div>
                          <p className="font-semibold text-sm">{c.name}</p>
                          <p className="text-xs text-slate-500">{c.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-7 py-5">
                      <div className="flex items-center gap-3">
                        <div className="w-24 h-1.5 bg-white/10 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full transition-all ${c.score > 75 ? 'bg-emerald-500' : c.score > 50 ? 'bg-amber-500' : 'bg-rose-500'}`}
                            style={{ width: `${c.score}%` }}
                          />
                        </div>
                        <span className={`px-3 py-1 rounded-lg text-xs font-bold ${getScoreBadge(c.score)}`}>
                          {c.score}%
                        </span>
                      </div>
                    </td>
                    <td className="px-7 py-5 text-sm text-slate-400 italic">{c.top_skill_gap}</td>
                    <td className="px-7 py-5">
                      <div className="flex items-center gap-2">
                        <div className={`w-1.5 h-1.5 rounded-full ${c.status === 'processed' ? 'bg-emerald-500' : 'bg-amber-500 animate-pulse'}`} />
                        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{c.status}</span>
                      </div>
                    </td>
                    <td className="px-7 py-5 text-right">
                      <div className="flex justify-end">
                        <div className="p-2 rounded-xl text-slate-600 group-hover:text-white group-hover:bg-indigo-500/20 transition-all">
                          <ArrowRight size={18} />
                        </div>
                      </div>
                    </td>
                  </motion.tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
