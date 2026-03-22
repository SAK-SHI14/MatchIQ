import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { Upload as UploadIcon, FileText, CheckCircle, Loader2, ArrowLeft, Plus } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Upload = () => {
  const [jdLoaded, setJdLoaded] = useState(null); // stores {id, title}
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [step, setStep] = useState(1); // 1: JD, 2: Resumes
  const navigate = useNavigate();

  // JD Form State
  const [jdForm, setJdForm] = useState({ title: '', text: '', skills: '' });

  const handleJdSubmit = async (e) => {
    e.preventDefault();
    setUploading(true);
    try {
      const res = await api.uploadJD(jdForm);
      setJdLoaded(res.data.data);
      setStep(2);
    } catch (err) {
      alert("Error uploading JD: " + err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (e) => {
    const selected = Array.from(e.target.files);
    setFiles(prev => [...prev, ...selected]);
  };

  const handleResumeUpload = async () => {
    if (!jdLoaded || files.length === 0) return;
    setUploading(true);
    let completed = 0;
    
    for (const file of files) {
      try {
        await api.uploadResume(jdLoaded.job_id, file);
        completed++;
        setProgress(Math.round((completed / files.length) * 100));
      } catch (err) {
        console.error(`Error uploading ${file.name}:`, err);
      }
    }
    
    setTimeout(() => navigate('/'), 1000);
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 flex flex-col items-center justify-center p-6 relative overflow-hidden font-sans">
      {/* Decorative Circles */}
      <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[600px] h-[600px] bg-cyan-500/10 rounded-full blur-[120px] pointer-events-none" />

      <header className="fixed top-8 left-8">
        <button 
          onClick={() => navigate('/')} 
          className="p-3 bg-slate-900 border border-white/10 rounded-2xl text-slate-400 hover:text-white transition-all flex items-center gap-2 hover:gap-3"
        >
          <ArrowLeft size={18} /> Back to Dashboard
        </button>
      </header>

      <main className="w-full max-w-2xl z-10">
        <AnimatePresence mode="wait">
          {step === 1 ? (
            <motion.div 
              key="step1"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-slate-900/60 backdrop-blur-2xl border border-white/10 rounded-[2.5rem] p-10 shadow-2xl"
            >
              <h2 className="text-3xl font-extrabold mb-2 tracking-tight">Step 1: Define Job</h2>
              <p className="text-slate-500 mb-8 font-medium italic">Paste the job description and requirements.</p>
              
              <form onSubmit={handleJdSubmit} className="space-y-6">
                <div>
                  <label className="block text-slate-400 text-xs font-bold uppercase mb-2 ml-1">Job Title</label>
                  <input 
                    type="text" 
                    required 
                    placeholder="e.g. Data Science Intern"
                    className="w-full bg-slate-800/50 border border-white/5 rounded-2xl py-4 px-6 focus:ring-2 focus:ring-indigo-500 placeholder:text-slate-600 outline-none"
                    value={jdForm.title}
                    onChange={e => setJdForm({...jdForm, title: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-slate-400 text-xs font-bold uppercase mb-2 ml-1">Job Description</label>
                  <textarea 
                    rows="4" 
                    required
                    placeholder="Describe the role responsibilities..."
                    className="w-full bg-slate-800/50 border border-white/5 rounded-2xl py-4 px-6 focus:ring-2 focus:ring-indigo-500 placeholder:text-slate-600 outline-none resize-none"
                    value={jdForm.text}
                    onChange={e => setJdForm({...jdForm, text: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-slate-400 text-xs font-bold uppercase mb-2 ml-1">Required Skills (Comma separated)</label>
                  <input 
                    type="text" 
                    required
                    placeholder="Python, ML, SQL, Pandas..."
                    className="w-full bg-slate-800/50 border border-white/5 rounded-2xl py-4 px-6 focus:ring-2 focus:ring-indigo-500 placeholder:text-slate-600 outline-none"
                    value={jdForm.skills}
                    onChange={e => setJdForm({...jdForm, skills: e.target.value})}
                  />
                </div>
                <button 
                  disabled={uploading}
                  className="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-bold shadow-xl shadow-indigo-500/20 transition-all flex items-center justify-center gap-2"
                >
                  {uploading ? <Loader2 className="animate-spin" /> : <CheckCircle size={20} />}
                  Save Job Profile
                </button>
              </form>
            </motion.div>
          ) : (
            <motion.div 
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-slate-900/60 backdrop-blur-2xl border border-white/10 rounded-[2.5rem] p-10 shadow-2xl"
            >
              <h2 className="text-3xl font-extrabold mb-2 tracking-tight">Step 2: Upload Resumes</h2>
              <p className="text-slate-500 mb-8 font-medium italic">Uploading candidates for: <span className="text-cyan-400 select-none">"{jdLoaded.title}"</span></p>
              
              <div 
                className="w-full py-16 px-10 border-2 border-dashed border-white/10 hover:border-indigo-500/40 hover:bg-indigo-500/[0.02] bg-slate-800/20 rounded-[2rem] transition-all relative flex flex-col items-center group cursor-pointer"
                onClick={() => document.getElementById('fileInput').click()}
              >
                <div className="w-16 h-16 bg-indigo-500/10 rounded-2xl flex items-center justify-center text-indigo-400 mb-4 group-hover:scale-110 transition-transform">
                  <UploadIcon size={32} />
                </div>
                <p className="font-bold text-lg mb-1">Click or drag & drop resumes</p>
                <p className="text-slate-500 text-sm">PDF or DOCX files supported</p>
                <input 
                  id="fileInput"
                  type="file" 
                  multiple 
                  className="absolute inset-0 opacity-0 cursor-pointer" 
                  onChange={handleFileChange}
                />
              </div>

              {files.length > 0 && (
                <div className="mt-8 space-y-3">
                  <p className="text-xs font-bold uppercase tracking-widest text-slate-500 ml-1">Selected Files ({files.length})</p>
                  <div className="max-h-40 overflow-y-auto pr-2 custom-scrollbar">
                    {files.map((f, i) => (
                      <div key={i} className="flex items-center gap-3 p-3 bg-slate-800/40 rounded-xl mb-2 text-sm border border-white/5">
                        <FileText size={16} className="text-slate-600" />
                        <span className="flex-grow truncate">{f.name}</span>
                        <span className="text-slate-600">{(f.size/1024).toFixed(0)} KB</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-10 space-y-6">
                {uploading && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs font-bold text-slate-400 px-1">
                      <span className="flex items-center gap-2"><Loader2 className="animate-spin" size={12} /> Processing with AI...</span>
                      <span>{progress}%</span>
                    </div>
                    <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                      <motion.div 
                        className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400"
                        initial={{ width: 0 }}
                        animate={{ width: `${progress}%` }}
                      />
                    </div>
                  </div>
                )}
                
                <button 
                  onClick={handleResumeUpload}
                  disabled={uploading || files.length === 0}
                  className="w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-2xl font-bold shadow-xl shadow-emerald-500/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Plus size={20} /> Start Intelligence Pipeline
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
};

export default Upload;
