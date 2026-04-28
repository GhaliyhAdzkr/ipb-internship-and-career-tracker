"""
Load Fixtures Script
Script untuk populate database dengan data dummy untuk testing
"""

import uuid

import click
from faker import Faker

from app_backend.models.users import Users
from app_backend.shared.database import Base, SessionLocal, engine
from app_backend.shared.security import hash_password

fake = Faker()


@click.command()
def load_fixtures():
    """Load fixtures ke database"""
    click.echo("Load fixtures dimulai")
    Base.metadata.drop_all(bind=engine)
    click.echo("Semua tabel berhasil dihapus")
    Base.metadata.create_all(bind=engine)
    click.echo("Semua tabel berhasil dibuat")

    try:
        with SessionLocal.begin() as db:
            click.echo("Mulai seeding database dengan data dummy")

            # Buat test students
            for i in range(5):
                db.add(
                    Users(
                        id=uuid.uuid4(),
                        email=fake.email(),
                        password_hash=hash_password("Password123!"),
                        role="STUDENT",
                        is_active=True,
                    )
                )

            # Buat default initial Admin account
            db.add(
                Users(
                    id=uuid.uuid4(),
                    email="admin@example.com",
                    password_hash=hash_password("Password123!"),
                    role="ADMIN",
                    is_active=True,
                )
            )

            click.echo("Selesai seeding database dengan data dummy")
            db.commit()
            click.echo("Fixture berhasil dimuat")
            click.echo("\nKredensial Admin untuk testing:")
            click.echo("Email: admin@example.com")
            click.echo("Password: Password123!")
    except Exception as e:
        click.echo(f"Error: {e}")
        db.rollback()
        click.echo("Error saat load fixtures!!!")
    finally:
        db.close()


if __name__ == "__main__":
    load_fixtures()
