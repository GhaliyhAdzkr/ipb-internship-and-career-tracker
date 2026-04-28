import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app_backend.features.analytics import (GetApplicationStatsCommand,
                                            GetDistributionCommand,
                                            GetVacancyStatsCommand,
                                            get_application_stats_command_handler,
                                            get_distribution_command_handler,
                                            get_vacancy_stats_command_handler)
from app_backend.schemas.analytics import (ApplicationStatsResponse,
                                           DistributionResponse,
                                           VacancyStatsResponse)
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import require_admin

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


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
    result = get_distribution_command_handler(
        command=GetDistributionCommand(department_id=department_id, year=year),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.error_message,
        )

    return DistributionResponse(
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


@router.get(
    "/applications",
    response_model=ApplicationStatsResponse,
    summary="Statistik lamaran keseluruhan",
)
def get_application_stats(
    current_user=Depends(require_admin),
    session: Session = Depends(get_session),
):
    result = get_application_stats_command_handler(
        command=GetApplicationStatsCommand(),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.error_message,
        )
    return ApplicationStatsResponse(
        total_applications=result.total_applications,
        status_breakdown=[
            {"status": s.status, "total": s.total}
            for s in result.status_breakdown
        ],
        conversion_rate=result.conversion_rate,
    )


@router.get(
    "/vacancies",
    response_model=VacancyStatsResponse,
    summary="Statistik lowongan",
)
def get_vacancy_stats(
    current_user=Depends(require_admin),
    session: Session = Depends(get_session),
):
    result = get_vacancy_stats_command_handler(
        command=GetVacancyStatsCommand(),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.error_message,
        )
    return VacancyStatsResponse(
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
