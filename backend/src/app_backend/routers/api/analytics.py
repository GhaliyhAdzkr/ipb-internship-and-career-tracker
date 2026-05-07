import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app_backend.features.analytics import (
    GetApplicationStatsCommand,
    GetDistributionCommand,
    GetVacancyStatsCommand,
    get_application_stats_command_handler,
    get_distribution_command_handler,
    get_vacancy_stats_command_handler,
)
from app_backend.schemas.analytics import ApplicationStatsResponse, DistributionResponse, VacancyStatsResponse
from app_backend.shared.auth_dependencies import require_admin
from app_backend.shared.cache import ANALYTICS_CACHE_TTL, cache_get, cache_set
from app_backend.shared.database import get_session

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


def _distribution_cache_key(department_id: Optional[uuid.UUID], year: Optional[int]) -> str:
    return f"analytics:distribution:{department_id}:{year}"


@router.get(
    "/distribution",
    response_model=DistributionResponse,
    summary="Dashboard distribusi penempatan magang",
)
def get_distribution(
    department_id: Optional[uuid.UUID] = None,
    year: Optional[int] = None,
    current_user=Depends(require_admin),
    session: Session = Depends(get_session),
):
    cache_key = _distribution_cache_key(department_id, year)
    cached = cache_get(cache_key)
    if cached:
        return DistributionResponse(**cached)

    result = get_distribution_command_handler(
        command=GetDistributionCommand(department_id=department_id, year=year),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.error_message,
        )

    response = DistributionResponse(
        total_placements=result.total_placements,
        top_companies=[
            {
                "company_id": item.company_id,
                "company_name": item.company_name,
                "company_industry": item.company_industry,
                "total_students": item.total_students,
            }
            for item in result.top_companies
        ],
        department_breakdown=[
            {
                "department_id": item.department_id,
                "department_name": item.department_name,
                "department_code": item.department_code,
                "company_id": item.company_id,
                "company_name": item.company_name,
                "total_students": item.total_students,
            }
            for item in result.department_breakdown
        ],
        compensation_breakdown=[
            {
                "payment_type": item.payment_type,
                "total": item.total,
            }
            for item in result.compensation_breakdown
        ],
        semester_trends=[
            {
                "year": item.year,
                "semester": item.semester,
                "total": item.total,
            }
            for item in result.semester_trends
        ],
        applied_filters={
            "department_id": str(department_id) if department_id else None,
            "year": year,
        },
    )
    cache_set(cache_key, response.model_dump(), ttl=ANALYTICS_CACHE_TTL)
    return response


@router.get(
    "/applications",
    response_model=ApplicationStatsResponse,
    summary="Statistik lamaran keseluruhan",
)
def get_application_stats(
    current_user=Depends(require_admin),
    session: Session = Depends(get_session),
):
    cache_key = "analytics:applications"
    cached = cache_get(cache_key)
    if cached:
        return ApplicationStatsResponse(**cached)

    result = get_application_stats_command_handler(
        command=GetApplicationStatsCommand(),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.error_message,
        )

    response = ApplicationStatsResponse(
        total_applications=result.total_applications,
        status_breakdown=[{"status": s.status, "total": s.total} for s in result.status_breakdown],
        conversion_rate=result.conversion_rate,
    )
    cache_set(cache_key, response.model_dump(), ttl=ANALYTICS_CACHE_TTL)
    return response


@router.get(
    "/vacancies",
    response_model=VacancyStatsResponse,
    summary="Statistik lowongan",
)
def get_vacancy_stats(
    current_user=Depends(require_admin),
    session: Session = Depends(get_session),
):
    cache_key = "analytics:vacancies"
    cached = cache_get(cache_key)
    if cached:
        return VacancyStatsResponse(**cached)

    result = get_vacancy_stats_command_handler(
        command=GetVacancyStatsCommand(),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.error_message,
        )

    response = VacancyStatsResponse(
        total_active_vacancies=result.total_active_vacancies,
        avg_applicants_per_vacancy=result.avg_applicants_per_vacancy,
        top_vacancies=[
            {
                "vacancy_id": v.vacancy_id,
                "title": v.title,
                "company_id": v.company_id,
                "total_applicants": v.total_applicants,
            }
            for v in result.top_vacancies
        ],
    )
    cache_set(cache_key, response.model_dump(), ttl=ANALYTICS_CACHE_TTL)
    return response
