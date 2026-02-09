"""
Domain Model untuk Placement
Model domain yang berisi business logic untuk penempatan magang/kerja
"""
import uuid
from datetime import date, datetime
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class PlacementStatus(str, Enum):
    """Enum untuk status placement"""
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"
    EXTENDED = "EXTENDED"


@dataclass
class Placement:
    """Domain model untuk Placement (Penempatan)"""
    
    id: uuid.UUID
    student_id: uuid.UUID
    company_id: uuid.UUID
    start_date: date
    end_date: date
    application_id: Optional[uuid.UUID] = None
    lecturer_id: Optional[uuid.UUID] = None
    status: str = PlacementStatus.ACTIVE.value
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validasi domain rules"""
        # Validasi status
        valid_statuses = [s.value for s in PlacementStatus]
        if self.status not in valid_statuses:
            raise ValueError(f"Status tidak valid. Pilih salah satu: {', '.join(valid_statuses)}")
        
        # Validasi tanggal
        if self.start_date >= self.end_date:
            raise ValueError("Tanggal selesai harus setelah tanggal mulai")
        
        # Tidak boleh tanggal di masa lalu (untuk placement baru)
        if self.created_at is None and self.start_date < date.today():
            raise ValueError("Tanggal mulai tidak boleh di masa lalu")
        
        # Set timestamp jika belum ada
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def complete(self):
        """Tandai placement sebagai selesai"""
        if self.status != PlacementStatus.ACTIVE.value:
            raise ValueError("Hanya placement ACTIVE yang bisa diselesaikan")
        
        # Cek apakah sudah melewati end_date
        if date.today() < self.end_date:
            raise ValueError("Placement belum mencapai tanggal selesai")
        
        self.status = PlacementStatus.COMPLETED.value
    
    def drop(self):
        """Mahasiswa mengundurkan diri dari placement"""
        if self.status not in [PlacementStatus.ACTIVE.value, PlacementStatus.EXTENDED.value]:
            raise ValueError("Hanya placement ACTIVE atau EXTENDED yang bisa di-drop")
        
        self.status = PlacementStatus.DROPPED.value
    
    def extend(self, new_end_date: date):
        """Perpanjang durasi placement"""
        if self.status not in [PlacementStatus.ACTIVE.value, PlacementStatus.EXTENDED.value]:
            raise ValueError("Hanya placement ACTIVE atau EXTENDED yang bisa diperpanjang")
        
        if new_end_date <= self.end_date:
            raise ValueError("Tanggal selesai baru harus lebih lama dari sekarang")
        
        self.end_date = new_end_date
        self.status = PlacementStatus.EXTENDED.value
    
    def assign_lecturer(self, lecturer_id: uuid.UUID):
        """Assign dosen pembimbing"""
        if self.status == PlacementStatus.DROPPED.value:
            raise ValueError("Tidak bisa assign dosen untuk placement yang di-drop")
        
        self.lecturer_id = lecturer_id
    
    def is_active(self) -> bool:
        """Cek apakah placement masih aktif"""
        return self.status in [PlacementStatus.ACTIVE.value, PlacementStatus.EXTENDED.value]
    
    def is_ongoing(self) -> bool:
        """Cek apakah placement sedang berlangsung (dalam periode waktu)"""
        today = date.today()
        return (self.is_active() and 
                self.start_date <= today <= self.end_date)
    
    def get_duration_days(self) -> int:
        """Hitung durasi placement dalam hari"""
        return (self.end_date - self.start_date).days
    
    def get_remaining_days(self) -> int:
        """Hitung sisa hari placement"""
        if not self.is_active():
            return 0
        
        today = date.today()
        if today > self.end_date:
            return 0
        
        return (self.end_date - today).days
