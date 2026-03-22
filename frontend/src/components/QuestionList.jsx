import React from 'react';
import { HelpCircle, ChevronRight, ClipboardCopy } from 'lucide-react';

const QuestionList = ({ questions }) => {
  const handleCopy = (q) => {
    navigator.clipboard.writeText(q);
    alert('Question copied to clipboard!');
  };

  return (
    <div className="space-y-4">
      {questions && questions.length > 0 ? (
        questions.map((q, idx) => (
          <div 
            key={idx} 
            className="group relative flex items-start gap-4 p-5 bg-slate-800/50 hover:bg-slate-800/80 transition-all rounded-2xl border border-white/5 shadow-md"
          >
            <div className="mt-1 flex-shrink-0 w-8 h-8 flex items-center justify-center bg-indigo-500/20 text-indigo-400 rounded-lg">
              <HelpCircle size={18} />
            </div>
            
            <div className="flex-grow">
              <p className="text-slate-200 text-sm leading-relaxed font-medium">
                {q}
              </p>
            </div>

            <button 
              onClick={() => handleCopy(q)}
              className="mt-1 p-2 text-slate-500 hover:text-white transition-opacity hidden group-hover:block"
              title="Copy to clipboard"
            >
              <ClipboardCopy size={16} />
            </button>
            <div className="mt-2 text-indigo-400 opacity-0 group-hover:opacity-100 transition-opacity">
              <ChevronRight size={16} />
            </div>
          </div>
        ))
      ) : (
        <div className="p-8 text-center text-slate-500 italic bg-slate-900/30 rounded-2xl border border-dashed border-white/10">
          No questions generated yet. Make sure the analysis is complete.
        </div>
      )}
    </div>
  );
};

export default QuestionList;
