import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import ScoreCard from '../components/ScoreCard';
import SkillGapChart from '../components/SkillGapChart';
import QuestionList from '../components/QuestionList';
import { ArrowLeft, Download, Briefcase, User, GraduationCap, Code, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const CandidateView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.getSkillGaps(id);
        const gapsData = res.data.data;
        
        // Fetch candidate details from match rankings (or a separate detail API)
        // For simplicity, we'll simulate fetching full details here
        // In a real app, GET /api/candidate/{id} would be used
        setCandidate({
          id: id,
          name: "Candidate Profile",
          email: "candidate@example.com",
          score: 82, // Placeholder, retrieve from match list or API
          gaps: gapsData || { missing_skills: [], importance_scores: {} },
          questions: [] // will fetch next
        });
        
        // Fetch questions
        const qRes = await api.getInterviewQuestions(id);
        setCandidate(prev => ({ ...prev, questions: qRes.data.data }));
        
      } catch (err) {
        console.error("Error fetching data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  if (loading) return (
    <div className="min-h-screen bg-[#020617] flex items-center justify-center text-slate-500">
      <div className="flex flex-col items-center gap-4">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
        Analysing candidate intelligence...
      </div>
    </div>
  );

  // Prepare radar chart data
  const radarData = [
    { skill: 'Python', candidate: 85, required: 90 },
    { skill: 'ML', candidate: 70, required: 95 },
    { skill: 'SQL', candidate: 90, required: 80 },
    { skill: 'Pandas', candidate: 80, required: 85 },
    { skill: 'Scikit', candidate: 60, required: 90 },
    { skill: 'Problem Solv.', candidate: 95, required: 100 },
  ];

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 p-8 font-sans pb-20">
      <header className="max-w-7xl mx-auto flex justify-between items-center mb-12">
        <button 
          onClick={() => navigate('/')} 
          className="p-3 bg-slate-900 border border-white/10 rounded-2xl text-slate-400 hover:text-white transition-all flex items-center gap-2 hover:gap-3"
        >
          <ArrowLeft size={18} /> Back to Dashboard
        </button>
        <button className="flex items-center gap-2 px-6 py-3 bg-indigo-600/10 border border-indigo-500/20 text-indigo-400 rounded-2xl font-bold hover:bg-indigo-600/20 transition-all">
          <Download size={18} /> Export Intel PDF
        </button>
      </header>

      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10">
        
        {/* Left Column: Match and Radar (4 cols) */}
        <aside className="lg:col-span-4 space-y-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center"
          >
            <ScoreCard score={candidate.score} />
            <div className="mt-8 w-full p-6 bg-slate-900/40 border border-white/5 rounded-[2.5rem]">
              <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-6 flex items-center gap-2">
                <Code size={14} className="text-indigo-400" /> Skill Overlap Analysis
              </h3>
              <SkillGapChart data={radarData} />
            </div>
          </motion.div>
        </aside>

        {/* Right Column: Details and Analysis (8 cols) */}
        <section className="lg:col-span-8 space-y-10">
          
          {/* Candidate Header */}
          <div className="flex justify-between items-end pb-8 border-b border-white/5">
            <div>
              <p className="text-sm font-bold text-indigo-400 uppercase tracking-widest mb-1 italic">Candidate Intelligence Report</p>
              <h1 className="text-5xl font-extrabold tracking-tighter flex items-center gap-4">
                {candidate.name} <User className="text-white/10" size={40} />
              </h1>
              <p className="mt-4 text-slate-400 flex items-center gap-6">
                <span className="flex items-center gap-2">
                  <Briefcase size={16} className="text-slate-600" /> Data Scientist
                </span>
                <span className="flex items-center gap-2">
                  <GraduationCap size={16} className="text-slate-600" /> MS Candidate
                </span>
                <span className="flex items-center gap-2 text-indigo-400 underline underline-offset-4 cursor-pointer">
                  {candidate.email}
                </span>
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Skill Gaps Card */}
            <div className="p-8 bg-slate-900/60 border border-white/10 rounded-[2.5rem] shadow-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                <AlertCircle size={80} />
              </div>
              <h3 className="text-lg font-extrabold mb-6 flex items-center gap-3">
                Identified Skill Gaps <span className="bg-rose-500/20 text-rose-400 text-[10px] px-2 py-0.5 rounded-full uppercase">Action Required</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {candidate.gaps?.missing_skills?.length > 0 ? (
                  candidate.gaps.missing_skills.map((skill, i) => (
                    <div 
                      key={i} 
                      className="px-4 py-2 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-xl text-sm font-semibold tracking-tight hover:scale-105 transition-transform cursor-help"
                      title={`Importance: ${candidate.gaps.importance_scores[skill] || 'High'}`}
                    >
                      {skill}
                    </div>
                  ))
                ) : (
                  <p className="text-slate-500 italic">No critical skill gaps identified.</p>
                )}
              </div>
            </div>

            {/* AI Summary Card */}
            <div className="p-8 bg-slate-900/60 border border-white/10 rounded-[2.5rem] shadow-2xl">
              <h3 className="text-lg font-extrabold mb-4 flex items-center gap-3">
                Recruiter Verdict <span className="text-slate-600 text-[10px] bg-white/5 px-2 py-0.5 rounded-full uppercase tracking-tighter">AI Analysis</span>
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Candidate shows strong fundamental proficiency in <span className="text-slate-200">Python</span> and <span className="text-slate-200">SQL</span>. 
                However, there is a notable gap in <span className="text-rose-400">Advanced ML Deployment</span> and <span className="text-rose-400">Scikit-learn Deep Dives</span>. 
                Recommended for initial screening focusing on data pipeline knowledge.
              </p>
            </div>
          </div>

          {/* Interview Questions Section */}
          <div className="space-y-6">
            <div className="flex items-center justify-between px-2">
              <h3 className="text-2xl font-extrabold tracking-tight">AI-Generated Interview Strategy</h3>
              <span className="text-xs font-bold text-slate-500 uppercase tracking-widest bg-slate-900 px-3 py-1 rounded-full border border-white/5">5 Targeted Questions</span>
            </div>
            <QuestionList questions={candidate.questions} />
          </div>

        </section>
      </main>
    </div>
  );
};

export default CandidateView;
