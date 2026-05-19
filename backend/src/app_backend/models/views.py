from sqlalchemy import BigInteger, Column, Date, String, Table

from app_backend.models.base import Base

t_view_internship_distribution = Table(
    "view_internship_distribution",
    Base.metadata,
    Column("company_name", String(150)),
    Column("company_industry", String(100)),
    Column("department_name", String(150)),
    Column("total_alumni_placed", BigInteger),
    Column("latest_placement_date", Date),
)
