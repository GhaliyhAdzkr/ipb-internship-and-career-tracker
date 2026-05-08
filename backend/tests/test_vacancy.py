"""
Tests: Vacancy Router – GET/POST /api/v1/vacancies/*, /api/v1/wishlist/*

Covers:
  Vacancy Management (Admin):
    POST /vacancies          – 201 success, 400 invalid company, 401 unauth
    GET /vacancies           – 200 list with pagination
    GET /vacancies/search    – 200 search with filters
    GET /vacancies/{id}      – 200 detail, 404 not found
    PUT /vacancies/{id}      – 200 update success, 404 not found
    DELETE /vacancies/{id}   – 204 success, 404 not found

  Wishlist Management (Student):
    POST /wishlist           – 201 success, 400 duplicate/inactive vacancy
    GET /wishlist            – 200 list with pagination
    GET /wishlist/{id}       – 200 detail, 404 not found
    PUT /wishlist/{id}       – 200 update notes
    DELETE /wishlist/{id}    – 204 success
"""

from __future__ import annotations

import uuid
from datetime import timedelta
from unittest.mock import MagicMock, patch

from tests.conftest import COMPANY_ID, NOW, SKILL_ID, STUDENT_USER_ID

#  Test Data

VACANCY_ID = uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")

VACANCY_PAYLOAD = {
    "company_id": str(COMPANY_ID),
    "title": "Software Engineer Intern",
    "description": "Mengembangkan aplikasi web menggunakan Python dan React",
    "type": "INTERNSHIP_GENERAL",
    "open_date": NOW.isoformat(),
    "close_date": (NOW + timedelta(days=30)).isoformat(),
    "location": "Jakarta, Indonesia",
    "payment_type": "PAID",
    "compensation_min": 1000000,
    "compensation_max": 2000000,
    "source_url": "https://example.com/job/123",
    "skills": [{"skill_id": str(SKILL_ID), "is_mandatory": True}],
}

WISHLIST_PAYLOAD = {
    "vacancy_id": str(VACANCY_ID),
    "notes": "Lowongan yang menarik untuk saya",
}

#  Vacancy: Create (Admin only)


def _make_vacancy_orm(vacancy_id=VACANCY_ID, company_id=COMPANY_ID):
    """Create mock Vacancy ORM object."""
    m = MagicMock()
    m.id = vacancy_id
    m.company_id = company_id
    m.title = "Software Engineer Intern"
    m.description = "Mengembangkan aplikasi web"
    m.type = "INTERNSHIP_GENERAL"
    m.open_date = NOW
    m.close_date = NOW + timedelta(days=30)
    m.location = "Jakarta"
    m.payment_type = "PAID"
    m.compensation_min = 1000000
    m.compensation_max = 2000000
    m.compensation_note = None
    m.source_url = "https://example.com"
    m.is_scraped = False
    m.is_auto_close = True
    m.is_active = True
    m.created_at = NOW
    m.updated_at = NOW
    return m


def test_create_vacancy_success(client_as_admin):
    with patch("app_backend.features.vacancy.vacancy_service.VacancyService.create_vacancy") as mock_method:
        from app_backend.schemas.vacancy import VacancyResponse

        mock_method.return_value = VacancyResponse(
            id=VACANCY_ID,
            company_id=COMPANY_ID,
            title="Software Engineer Intern",
            description="Mengembangkan aplikasi web",
            type="INTERNSHIP_GENERAL",
            open_date=NOW,
            close_date=NOW + timedelta(days=30),
            location="Jakarta",
            payment_type="PAID",
            compensation_min=1000000,
            compensation_max=2000000,
            compensation_note=None,
            source_url="https://example.com",
            is_scraped=False,
            is_auto_close=True,
            is_active=True,
            created_at=NOW,
            updated_at=NOW,
        )
        resp = client_as_admin.post("/api/v1/vacancies", json=VACANCY_PAYLOAD)

    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Software Engineer Intern"
    assert data["is_active"] is True


def test_create_vacancy_unauthenticated(client_no_auth):
    resp = client_no_auth.post("/api/v1/vacancies", json=VACANCY_PAYLOAD)
    assert resp.status_code == 401  # No auth token


def test_create_vacancy_as_student_forbidden(client_as_student):
    resp = client_as_student.post("/api/v1/vacancies", json=VACANCY_PAYLOAD)
    assert resp.status_code == 403


def test_create_vacancy_invalid_company(client_as_admin):
    with patch("app_backend.features.vacancy.vacancy_service.VacancyService.create_vacancy") as mock_method:
        mock_method.side_effect = ValueError("Perusahaan tidak ditemukan")
        resp = client_as_admin.post("/api/v1/vacancies", json=VACANCY_PAYLOAD)

    assert resp.status_code == 400
    assert "Perusahaan tidak ditemukan" in resp.json()["detail"]


#  Vacancy: List


def test_list_vacancies_success(client_as_student):
    with patch("app_backend.features.vacancy.vacancy_service.VacancyService.list_active_vacancies") as mock_method:
        mock_method.return_value = []
        resp = client_as_student.get("/api/v1/vacancies")

    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


def test_list_vacancies_with_pagination(client_as_student):
    with patch("app_backend.features.vacancy.vacancy_service.VacancyService.list_active_vacancies") as mock_method:
        mock_method.return_value = []
        resp = client_as_student.get("/api/v1/vacancies?page=2&per_page=5")

    assert resp.status_code == 200
    assert resp.json()["page"] == 2


#  Vacancy: Search


def test_search_vacancies_by_query(client_as_student):
    with patch("app_backend.routers.api.vacancy.search_vacancies_command_handler") as mock_handler:
        from app_backend.schemas.vacancy import VacancyListResponse

        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            data=VacancyListResponse(
                items=[],
                total=0,
                page=1,
                per_page=10,
                total_pages=1,
            ),
        )
        resp = client_as_student.get("/api/v1/vacancies/search?query=python")

    assert resp.status_code == 200


def test_search_vacancies_by_location(client_as_student):
    with patch("app_backend.routers.api.vacancy.search_vacancies_command_handler") as mock_handler:
        from app_backend.schemas.vacancy import VacancyListResponse

        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            data=VacancyListResponse(
                items=[],
                total=0,
                page=1,
                per_page=10,
                total_pages=1,
            ),
        )
        resp = client_as_student.get("/api/v1/vacancies/search?location=Jakarta")

    assert resp.status_code == 200


def test_search_vacancies_by_type(client_as_student):
    with patch("app_backend.routers.api.vacancy.search_vacancies_command_handler") as mock_handler:
        from app_backend.schemas.vacancy import VacancyListResponse

        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            data=VacancyListResponse(
                items=[],
                total=0,
                page=1,
                per_page=10,
                total_pages=1,
            ),
        )
        resp = client_as_student.get("/api/v1/vacancies/search?type=INTERNSHIP_GENERAL")

    assert resp.status_code == 200


#  Vacancy: Get Detail


def test_get_vacancy_detail_success(client_as_student):
    with patch("app_backend.features.vacancy.vacancy_service.VacancyService.get_vacancy") as mock_method:
        from app_backend.schemas.vacancy import CompanyInfo, VacancyDetailResponse

        mock_method.return_value = VacancyDetailResponse(
            id=VACANCY_ID,
            company=CompanyInfo(
                id=COMPANY_ID,
                name="PT Tech Indonesia",
                industry="Technology",
                website_url="https://techindo.co.id",
            ),
            title="Software Engineer Intern",
            description="Mengembangkan aplikasi web",
            type="INTERNSHIP_GENERAL",
            open_date=NOW,
            close_date=NOW + timedelta(days=30),
            location="Jakarta",
            payment_type="PAID",
            compensation_min=1000000,
            compensation_max=2000000,
            compensation_note=None,
            source_url="https://example.com",
            is_scraped=False,
            is_auto_close=True,
            is_active=True,
            skills=[],
            created_at=NOW,
            updated_at=NOW,
        )
        resp = client_as_student.get(f"/api/v1/vacancies/{VACANCY_ID}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Software Engineer Intern"
    assert data["company"]["name"] == "PT Tech Indonesia"


def test_get_vacancy_not_found(client_as_student):
    with patch("app_backend.features.vacancy.vacancy_service.VacancyService.get_vacancy") as mock_method:
        mock_method.return_value = None
        resp = client_as_student.get(f"/api/v1/vacancies/{uuid.uuid4()}")

    assert resp.status_code == 404


#  Vacancy: Update (Admin only)


def test_update_vacancy_success(client_as_admin):
    with patch("app_backend.features.vacancy.vacancy_service.VacancyService.update_vacancy") as mock_method:
        from app_backend.schemas.vacancy import VacancyResponse

        mock_method.return_value = VacancyResponse(
            id=VACANCY_ID,
            company_id=COMPANY_ID,
            title="Updated Title",
            description="Updated description",
            type="INTERNSHIP_GENERAL",
            open_date=NOW,
            close_date=NOW + timedelta(days=30),
            location="Jakarta",
            payment_type="PAID",
            compensation_min=1000000,
            compensation_max=2000000,
            compensation_note=None,
            source_url="https://example.com",
            is_scraped=False,
            is_auto_close=True,
            is_active=True,
            created_at=NOW,
            updated_at=NOW,
        )
        resp = client_as_admin.put(
            f"/api/v1/vacancies/{VACANCY_ID}",
            json={"title": "Updated Title"},
        )

    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Title"


def test_update_vacancy_as_student_forbidden(client_as_student):
    resp = client_as_student.put(
        f"/api/v1/vacancies/{VACANCY_ID}",
        json={"title": "Updated Title"},
    )
    assert resp.status_code == 403


#  Vacancy: Delete (Admin only)


def test_delete_vacancy_success(client_as_admin):
    with patch("app_backend.features.vacancy.vacancy_service.VacancyService.delete_vacancy") as mock_method:
        mock_method.return_value = None
        resp = client_as_admin.delete(f"/api/v1/vacancies/{VACANCY_ID}")

    assert resp.status_code == 204


def test_delete_vacancy_not_found(client_as_admin):
    with patch("app_backend.features.vacancy.vacancy_service.VacancyService.delete_vacancy") as mock_method:
        mock_method.side_effect = ValueError("Lowongan tidak ditemukan")
        resp = client_as_admin.delete(f"/api/v1/vacancies/{uuid.uuid4()}")

    assert resp.status_code == 404


#  Wishlist: Add (Student only)

WISHLIST_ID = uuid.UUID("99999999-9999-9999-9999-999999999999")


def _make_wishlist_orm(wishlist_id=WISHLIST_ID, student_id=STUDENT_USER_ID):
    """Create mock Wishlist ORM object."""
    m = MagicMock()
    m.id = wishlist_id
    m.student_id = student_id
    m.vacancy_id = VACANCY_ID
    m.notes = "Lowongan yang menarik"
    m.created_at = NOW
    return m


def test_add_wishlist_success(client_as_student):
    with patch("app_backend.routers.api.vacancy.add_wishlist_command_handler") as mock_handler:
        from app_backend.schemas.wishlist import WishlistResponse

        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            wishlist=WishlistResponse(
                id=WISHLIST_ID,
                student_id=STUDENT_USER_ID,
                vacancy_id=VACANCY_ID,
                notes="Lowongan yang menarik",
                created_at=NOW,
            ),
        )
        resp = client_as_student.post("/api/v1/wishlist", json=WISHLIST_PAYLOAD)

    assert resp.status_code == 201
    assert resp.json()["vacancy_id"] == str(VACANCY_ID)


def test_add_wishlist_as_admin_forbidden(client_as_admin_for_student_only):
    resp = client_as_admin_for_student_only.post("/api/v1/wishlist", json=WISHLIST_PAYLOAD)
    assert resp.status_code == 403


def test_add_wishlist_duplicate(client_as_student):
    with patch("app_backend.routers.api.vacancy.add_wishlist_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            got_error=lambda: True,
            error_message="Lowongan sudah ada di wishlist",
        )
        resp = client_as_student.post("/api/v1/wishlist", json=WISHLIST_PAYLOAD)

    assert resp.status_code == 400


#  Wishlist: List


def test_list_wishlist_success(client_as_student):
    with patch("app_backend.routers.api.vacancy.list_wishlist_command_handler") as mock_handler:
        from app_backend.schemas.wishlist import WishlistListResponse

        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            data=WishlistListResponse(
                items=[],
                total=0,
            ),
        )
        resp = client_as_student.get("/api/v1/wishlist")

    assert resp.status_code == 200
    assert "items" in resp.json()


def test_list_wishlist_as_admin_forbidden(client_as_admin_for_student_only):
    resp = client_as_admin_for_student_only.get("/api/v1/wishlist")
    assert resp.status_code == 403


#  Wishlist: Get Detail


def test_get_wishlist_detail_success(client_as_student):
    with patch("app_backend.routers.api.vacancy.get_wishlist_command_handler") as mock_handler:
        from app_backend.schemas.wishlist import VacancySummary, WishlistDetailResponse

        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            wishlist=WishlistDetailResponse(
                id=WISHLIST_ID,
                student_id=STUDENT_USER_ID,
                vacancy=VacancySummary(
                    id=VACANCY_ID,
                    title="Software Engineer",
                    location="Jakarta",
                    type="INTERNSHIP_GENERAL",
                    payment_type="PAID",
                    open_date=NOW,
                    close_date=NOW + timedelta(days=30),
                ),
                notes="Catatan saya",
                created_at=NOW,
            ),
        )
        resp = client_as_student.get(f"/api/v1/wishlist/{WISHLIST_ID}")

    assert resp.status_code == 200
    assert resp.json()["vacancy"]["title"] == "Software Engineer"


def test_get_wishlist_not_found(client_as_student):
    with patch("app_backend.routers.api.vacancy.get_wishlist_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            got_error=lambda: True,
            error_message="Wishlist tidak ditemukan",
        )
        resp = client_as_student.get(f"/api/v1/wishlist/{uuid.uuid4()}")

    assert resp.status_code == 404


#  Wishlist: Update


def test_update_wishlist_notes_success(client_as_student):
    with patch("app_backend.routers.api.vacancy.update_wishlist_command_handler") as mock_handler:
        from app_backend.schemas.wishlist import WishlistResponse

        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            wishlist=WishlistResponse(
                id=WISHLIST_ID,
                student_id=STUDENT_USER_ID,
                vacancy_id=VACANCY_ID,
                notes="Updated notes",
                created_at=NOW,
            ),
        )
        resp = client_as_student.put(
            f"/api/v1/wishlist/{WISHLIST_ID}",
            json={"notes": "Updated notes"},
        )

    assert resp.status_code == 200
    assert resp.json()["notes"] == "Updated notes"


def test_update_wishlist_not_owner(client_as_student):
    with patch("app_backend.routers.api.vacancy.update_wishlist_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            got_error=lambda: True,
            error_message="Tidak berhak mengubah wishlist ini",
        )
        resp = client_as_student.put(
            f"/api/v1/wishlist/{WISHLIST_ID}",
            json={"notes": "Hacked notes"},
        )

    assert resp.status_code == 400


#  Wishlist: Delete


def test_delete_wishlist_success(client_as_student):
    with patch("app_backend.routers.api.vacancy.delete_wishlist_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            success=True,
            got_error=lambda: False,
        )
        resp = client_as_student.delete(f"/api/v1/wishlist/{WISHLIST_ID}")

    assert resp.status_code == 204


def test_delete_wishlist_not_owner(client_as_student):
    with patch("app_backend.routers.api.vacancy.delete_wishlist_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            success=False,
            got_error=lambda: True,
            error_message="Tidak berhak menghapus wishlist ini",
        )
        resp = client_as_student.delete(f"/api/v1/wishlist/{uuid.uuid4()}")

    assert resp.status_code == 400
