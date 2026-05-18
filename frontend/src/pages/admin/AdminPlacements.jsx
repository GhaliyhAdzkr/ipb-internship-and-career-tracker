import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { id } from 'date-fns/locale';
import adminService from '../../services/adminService';
import { 
  PiMagnifyingGlass,
  PiBuildings,
  PiCalendarBlank,
  PiUserList,
  PiSpinnerGap,
  PiWarning
} from 'react-icons/pi';

function AdminPlacements() {
  const [searchTerm, setSearchTerm] = useState("");

  const { data: placements = [], isLoading, isError } = useQuery({
    queryKey: ['admin', 'placements'],
    queryFn: adminService.getPlacements,
  });

  const filteredPlacements = placements.filter(placement => {
    // We don't have student name in PlacementResponse by default unless backend joins it. 
    // Usually company_name or status is what we filter by.
    const term = searchTerm.toLowerCase();
    const companyMatch = placement.company_name?.toLowerCase().includes(term);
    const statusMatch = placement.status?.toLowerCase().includes(term);
    return companyMatch || statusMatch;
  });

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center font-jakarta">
        <PiSpinnerGap size={40} className="animate-spin text-sky-950" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="h-full flex items-center justify-center font-jakarta">
        <div className="flex flex-col items-center gap-2 text-rose-600">
          <PiWarning size={48} />
          <p className="font-bold">Gagal memuat data penempatan.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="font-jakarta">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-sky-950">Data Penempatan (Placement)</h1>
        <p className="text-zinc-500 mt-2">Daftar seluruh mahasiswa yang sedang menjalankan program magang.</p>
      </div>

      {/* Header Actions */}
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-6 bg-white p-4 rounded-xl shadow-sm border border-slate-100">
        <div className="relative w-full md:w-96">
          <PiMagnifyingGlass className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400" size={20} />
          <input
            type="text"
            placeholder="Cari berdasarkan perusahaan atau status..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-12 pr-4 py-2.5 bg-zinc-50 border border-zinc-200 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 outline-none transition-all"
          />
        </div>
        <div className="flex items-center gap-2 text-sm font-bold text-sky-950 bg-sky-50 px-4 py-2.5 rounded-lg border border-sky-100">
          <PiUserList size={20} />
          Total Penempatan: {filteredPlacements.length}
        </div>
      </div>

      {/* Content */}
      {filteredPlacements.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-xl shadow-sm border border-slate-100">
          <PiBuildings size={64} className="mx-auto text-zinc-300 mb-4" />
          <h2 className="text-xl font-bold text-slate-700">Tidak Ada Data</h2>
          <p className="text-slate-500 mt-2">Belum ada penempatan yang sesuai dengan pencarian Anda.</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-sky-950 text-white">
                <tr>
                  <th className="p-4 font-bold">Mahasiswa (ID)</th>
                  <th className="p-4 font-bold">Perusahaan</th>
                  <th className="p-4 font-bold">Periode Magang</th>
                  <th className="p-4 font-bold">Pembimbing Lapangan</th>
                  <th className="p-4 font-bold">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredPlacements.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-4">
                      <div className="font-bold text-sky-950">{p.student_id.substring(0, 8).toUpperCase()}</div>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <PiBuildings size={18} className="text-zinc-400" />
                        <span className="font-bold text-slate-700">{p.company_name || "Perusahaan"}</span>
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-2 text-slate-600">
                        <PiCalendarBlank size={16} />
                        <span>
                          {format(new Date(p.start_date), "dd MMM yyyy", { locale: id })} - {format(new Date(p.end_date), "dd MMM yyyy", { locale: id })}
                        </span>
                      </div>
                    </td>
                    <td className="p-4 text-slate-600">
                      {p.external_supervisor_name || "-"}
                    </td>
                    <td className="p-4">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded text-xs font-bold uppercase ${
                        p.status === "ACTIVE" 
                          ? "bg-emerald-100 text-emerald-800" 
                          : "bg-slate-100 text-slate-800"
                      }`}>
                        {p.status === "ACTIVE" ? "Aktif" : p.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default AdminPlacements;
