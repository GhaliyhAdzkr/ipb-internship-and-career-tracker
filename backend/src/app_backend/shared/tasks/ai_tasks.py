"""
AI Tasks – Background tasks untuk fitur AI menggunakan LangChain/LangGraph.
Berjalan di queue terpisah untuk tidak blocking main API.
"""

import uuid
from typing import Dict, List, Optional

from celery import shared_task
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel

# Simple in-memory LLM (bisa diganti dengan API key untuk production)
# Untuk production, gunakan: from langchain.chat_models import ChatOpenAI

class TaskResult(BaseModel):
    """Result model untuk task"""
    success: bool
    result: Optional[Dict] = None
    error: Optional[str] = None


def get_llm():
    """
    Get LLM instance.
    Untuk production, gunakan environment variable untuk API key.
    """
    # Placeholder, untuk production gunakan:
    # from langchain_community.chat_models import ChatOpenAI
    # return ChatOpenAI(temperature=0.7, model="gpt-4")
    return None


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def parse_cv_skills(
    self,
    student_id: str,
    cv_url: str,
) -> Dict:
    """
    Task: Parse CV PDF untuk ekstrak skills otomatis.
    Menggunakan LangChain untuk extraction.
    """
    try:
        # Validate inputs
        if not student_id or not cv_url:
            return TaskResult(success=False, error="Invalid inputs").dict()

        # For now, return placeholder - implementasi lengkap memerlukan:
        # 1. Download PDF dari URL
        # 2. Extract text menggunakan pypdf
        # 3. Parse dengan LLM
        
        # Placeholder implementation
        result = {
            "student_id": student_id,
            "extracted_skills": [
                {"name": "Python", "category": "Programming Language", "confidence": 0.9},
                {"name": "SQL", "category": "Database", "confidence": 0.85},
            ],
            "status": "completed",
        }

        return TaskResult(success=True, result=result).dict()

    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def enhance_log_description(
    self,
    log_id: str,
    raw_description: str,
) -> Dict:
    """
    Task: Enhance log description menggunakan AI.
    Mengubah bahasa informal ke bahasa profesional.
    """
    try:
        if not log_id or not raw_description:
            return TaskResult(success=False, error="Invalid inputs").dict()

        # Prompt untuk enhancement
        enhance_prompt = PromptTemplate(
            input_variables=["raw_text"],
            template="""
Teks berikut adalah draf kegiatan magang. 
Tolong perbaiki tata bahasa dan struktur bahasa menjadi lebih profesional dengan format bahasa indonesia yang baik dan benar.
Tetap jaga makna asli dan pastikan hasil teksnya tidak terlalu panjang, cukup ringkas dan jelas.

Draf: {raw_text}

Teks yang sudah diperbaiki:
"""
        )

        # For now, return placeholder
        # Production: Gunakan LLM untuk enhance
        result = {
            "log_id": log_id,
            "original": raw_description,
            "enhanced": f"{raw_description} [Ditingkatkan oleh AI]",
            "status": "completed",
        }

        return TaskResult(success=True, result=result).dict()

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def match_job_skills(
    self,
    student_id: str,
    vacancy_id: str,
) -> Dict:
    """
    Task: Calculate job matching score berdasarkan skills.
    Compares student skills vs vacancy requirements.
    """
    try:
        if not student_id or not vacancy_id:
            return TaskResult(success=False, error="Invalid inputs").dict()

        # For now, return placeholder
        # Production: Ambil student skills dan vacancy skills dari DB
        # Hitung match percentage
        result = {
            "student_id": student_id,
            "vacancy_id": vacancy_id,
            "match_percentage": 75.0,
            "matched_skills": ["Python", "SQL"],
            "missing_skills": ["Java"],
            "total_required": 3,
            "total_matched": 2,
            "status": "completed",
        }

        return TaskResult(success=True, result=result).dict()

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task
def batch_process_cv_parsing(student_ids: List[str]) -> Dict:
    """
    Batch process CV parsing untuk multiple students.
    """
    results = []
    for student_id in student_ids:
        # Get student profile untuk dapat CV URL
        # Process CV dan simpan skills
        results.append({
            "student_id": student_id,
            "status": "queued",
        })
    
    return {
        "total": len(student_ids),
        "processed": 0,
        "results": results,
    }
