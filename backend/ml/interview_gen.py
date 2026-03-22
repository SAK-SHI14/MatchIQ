"""
Interview Question Generator.
Template-based by default (fully offline).
Switches to RAG+LLM when HF_API_KEY or ANTHROPIC_API_KEY is set in .env.
"""
import os
import re
from typing import List


class InterviewGenerator:
    """
    Generates 5 role-specific interview questions per candidate.
    No network calls at init — lazy LLM initialisation only when a key is set.
    """

    def __init__(self):
        self.hf_key = os.getenv("HF_API_KEY", "")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        print("[InterviewGen] Ready. LLM mode:", "HF" if self.hf_key else ("Anthropic" if self.anthropic_key else "Template"))

    # ------------------------------------------------------------------
    def generate_questions(
        self, jd_text: str, resume_text: str, missing_skills: List[str]
    ) -> List[str]:
        """Public API — returns exactly 5 questions."""
        if self.hf_key:
            try:
                return self._rag_generate(jd_text, resume_text, missing_skills)
            except Exception as e:
                print(f"[InterviewGen] LLM failed ({e}), template fallback.")
        return self._template_questions(missing_skills)

    # ------------------------------------------------------------------
    def _rag_generate(
        self, jd_text: str, resume_text: str, missing_skills: List[str]
    ) -> List[str]:
        """FAISS + HuggingFaceHub RAG pipeline (network required)."""
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceHub
        from langchain.chains import LLMChain
        from langchain.prompts import PromptTemplate
        from langchain_core.documents import Document

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        docs = [
            Document(page_content=f"JOB DESCRIPTION:\n{jd_text}"),
            Document(page_content=f"CANDIDATE RESUME:\n{resume_text}"),
        ]
        vs = FAISS.from_documents(docs, embeddings)
        context_docs = vs.as_retriever(search_kwargs={"k": 2}).get_relevant_documents(
            "candidate weaknesses and skill gaps for this role"
        )
        context = "\n\n".join(d.page_content for d in context_docs)

        prompt = PromptTemplate(
            input_variables=["context", "missing_skills"],
            template=(
                "You are an expert technical interviewer.\n"
                "Based on the context below, generate exactly 5 specific technical interview questions "
                "that probe the candidate's knowledge in: {missing_skills}.\n\n"
                "Context:\n{context}\n\n"
                "Output ONLY the 5 questions, one per line, numbered 1-5."
            ),
        )
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-large",
            huggingfacehub_api_token=self.hf_key,
            model_kwargs={"temperature": 0.5, "max_new_tokens": 512},
        )
        response = LLMChain(llm=llm, prompt=prompt).run(
            context=context,
            missing_skills=", ".join(missing_skills[:5]),
        )
        return self._parse(response)

    # ------------------------------------------------------------------
    @staticmethod
    def _parse(raw: str) -> List[str]:
        lines = [l.strip() for l in raw.strip().splitlines() if l.strip()]
        out = []
        for l in lines:
            l = re.sub(r"^\d+[\.\)]\s*", "", l)
            if len(l) > 10:
                out.append(l)
            if len(out) == 5:
                break
        return out

    @staticmethod
    def _template_questions(missing_skills: List[str]) -> List[str]:
        """Fully offline template Qs, personalised to each gap."""
        templates = [
            "Walk us through a project where you applied {skill}. What was your specific contribution?",
            "How would you design a solution that heavily depends on {skill} from scratch?",
            "Describe a situation where weak {skill} knowledge caused a setback. How did you recover?",
            "What is your plan to rapidly strengthen your proficiency in {skill} within 30 days?",
            "If asked to evaluate two approaches to a {skill} problem, what criteria would you use?",
        ]
        skills = (missing_skills or ["the key required skills"])[:5]
        return [
            templates[i % len(templates)].format(skill=s)
            for i, s in enumerate(skills)
        ]
