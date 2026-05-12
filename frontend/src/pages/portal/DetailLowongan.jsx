import React from 'react';
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate, useParams, Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { vacancyService } from "../../services/vacancyService";
import { format } from 'date-fns';
import {
  PiBriefcase,
  PiMapPin,
  PiClock,
  PiCalendarBlank,
  PiBookmarkSimple,
  PiArrowLeft,
  PiSpinnerGap,
  PiCheckCircleFill,
  PiInfo,
  PiBuildings,
  PiGlobe,
  PiCaretRightBold,
  PiSealCheckFill,
  PiChartBarFill
} from "react-icons/pi";

export default function DetailLowongan() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { vacancyId } = useParams();
  const token = localStorage.getItem('token');

  const vacancyQuery = useQuery({
    queryKey: ["vacancy", vacancyId],
    queryFn: () => vacancyService.getVacancy(vacancyId),
    enabled: !!vacancyId,
  });

  const jobMatchQuery = useQuery({
    queryKey: ["jobmatch", vacancyId],
    queryFn: () => vacancyService.getJobMatch(vacancyId),
    enabled: !!vacancyId && !!token,
    staleTime: 1000 * 60 * 5,
  });

  const saveWishlistMutation = useMutation({
    mutationFn: () => vacancyService.addToWishlist(vacancyId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["vacancy", vacancyId] });
      alert("Lowongan berhasil disimpan ke wishlist.");
    },
    onError: (error) => {
      alert(error.response?.data?.detail || "Gagal menyimpan ke wishlist.");
    },
  });

  const vacancy = vacancyQuery.data;
  const match = jobMatchQuery.data;

  const displayType = (value) => {
    const types = {
      "INTERNSHIP_GENERAL": "Magang Umum",
      "MBKM_INTERNSHIP": "MBKM Magang",
      "MBKM_STUDY_INDEPENDENT": "MBKM Studi Independen",
      "FULL_TIME": "Full Time"
    };
    return types[value] || value || "-";
  };

  const displayPayment = (value) => {
    const payments = {
      "PAID": "Berbayar (Paid)",
      "UNPAID": "Sukarela (Unpaid)",
      "ALLOWANCE_ONLY": "Allowance / Uang Saku"
    };
    return payments[value] || value || "-";
  };

  if (vacancyQuery.isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="flex flex-col items-center gap-4">
          <PiSpinnerGap size={48} className="animate-spin text-sky-600" />
          <p className="text-sm font-bold text-sky-950/40 uppercase tracking-[0.2em]">Memuat Detail...</p>
        </div>
      </div>
    );
  }

  if (vacancyQuery.isError || !vacancy) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-white p-6">
        <div className="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center text-red-500 mb-6">
          <PiInfo size={40} />
        </div>
        <h2 className="text-2xl font-[900] text-sky-950 mb-2">Lowongan Tidak Ditemukan</h2>
        <p className="text-slate-500 mb-8 text-center max-w-md">
          Maaf, lowongan yang Anda cari mungkin sudah berakhir atau link yang Anda gunakan salah.
        </p>
        <button 
          onClick={() => navigate("/lowongan")} 
          className="bg-sky-950 text-white px-8 py-3 rounded-xl font-bold hover:bg-sky-900 transition-all active:scale-95"
        >
          Kembali ke Jelajah Lowongan
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FBFDFF] font-jakarta pb-20">
      {/* Header / Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <button 
            onClick={() => navigate(-1)} 
            className="group flex items-center gap-2 text-slate-500 hover:text-sky-950 transition-colors font-bold text-sm"
          >
            <PiArrowLeft size={18} className="group-hover:-translate-x-1 transition-transform" />
            Kembali
          </button>
          
          <div className="flex items-center gap-4">
            <Link to="/" className="flex items-center gap-2">
              <img src="/logo/laras.png" alt="LARAS" className="w-8 h-8 object-contain" />
              <span className="text-[18px] font-[1000] text-sky-950 tracking-tighter">
                LARAS<span className="text-sky-600">.</span>
              </span>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="relative bg-white border-b border-slate-100 pt-12 pb-16 overflow-hidden">
        {/* Decorative Background */}
        <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-sky-50/50 to-transparent pointer-events-none" />
        
        <div className="max-w-7xl mx-auto px-6 relative z-10">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
            <div className="flex gap-6 items-start md:items-center">
              <motion.div 
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                className="w-20 h-20 md:w-24 md:h-24 bg-white rounded-[28px] border border-slate-100 shadow-xl shadow-sky-900/5 flex items-center justify-center p-4 shrink-0 overflow-hidden"
              >
                {vacancy.company?.logo_url ? (
                  <img 
                    src={vacancy.company.logo_url} 
                    alt={vacancy.company.name} 
                    className="w-full h-auto max-h-full object-contain" 
                    referrerPolicy="no-referrer"
                  />
                ) : (
                  <div className="text-3xl font-[900] text-sky-200">{vacancy.company?.name?.charAt(0)}</div>
                )}
              </motion.div>
              
              <div>
                <motion.div 
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center gap-2 mb-2"
                >
                  <span className="bg-sky-50 text-sky-700 text-[10px] font-extrabold px-3 py-1 rounded-full uppercase tracking-widest border border-sky-100/50">
                    {displayType(vacancy.type)}
                  </span>
                  {vacancy.is_active && (
                    <span className="flex items-center gap-1 text-[10px] font-bold text-emerald-500 uppercase tracking-wider">
                      <PiSealCheckFill size={14} />
                      Aktif
                    </span>
                  )}
                </motion.div>
                
                <motion.h1 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="text-3xl md:text-4xl font-[1000] text-sky-950 mb-2 tracking-tight"
                >
                  {vacancy.title}
                </motion.h1>
                
                <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  className="flex flex-wrap items-center gap-y-2 gap-x-6 text-slate-500 font-medium text-[15px]"
                >
                  <div className="flex items-center gap-2">
                    <PiBuildings className="text-sky-400" size={20} />
                    <span className="text-sky-950 font-bold">{vacancy.company?.name || 'Perusahaan'}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <PiMapPin className="text-slate-300" size={20} />
                    <span>{vacancy.location || '-'}</span>
                  </div>
                </motion.div>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
              {token ? (
                <button 
                  onClick={() => saveWishlistMutation.mutate()}
                  disabled={saveWishlistMutation.isPending}
                  className="bg-white text-sky-950 border border-slate-200 px-6 py-4 rounded-2xl font-bold flex items-center justify-center gap-2 hover:bg-slate-50 transition-all active:scale-95"
                >
                  <PiBookmarkSimple size={22} />
                  <span>Simpan</span>
                </button>
              ) : null}
              
              <a 
                href={vacancy.source_url || "#"} 
                target="_blank" 
                rel="noreferrer"
                className="bg-sky-950 text-white px-10 py-4 rounded-2xl font-bold flex items-center justify-center gap-2 hover:bg-sky-900 transition-all active:scale-95 shadow-xl shadow-sky-900/20"
              >
                <span>Lamar Sekarang</span>
                <PiCaretRightBold size={18} />
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 mt-12">
        <div className="grid lg:grid-cols-3 gap-12">
          {/* Left Column: Details */}
          <div className="lg:col-span-2 space-y-12">
            {/* Job Match Score (Guest Protection) */}
            {token && match && (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gradient-to-br from-sky-950 to-sky-900 rounded-[32px] p-8 text-white relative overflow-hidden shadow-2xl shadow-sky-950/20"
              >
                <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sky-300 text-xs font-bold uppercase tracking-[0.2em]">
                      <PiChartBarFill size={18} />
                      AI Talent Matching
                    </div>
                    <h3 className="text-2xl font-[900]">Kesesuaian Profil Anda</h3>
                    <p className="text-sky-200/70 text-sm max-w-sm">
                      Berdasarkan skill dan kualifikasi Anda, sistem kami menghitung tingkat kecocokan dengan posisi ini.
                    </p>
                  </div>
                  
                  <div className="flex items-center gap-6">
                    <div className="w-24 h-24 rounded-full border-[6px] border-sky-800 flex items-center justify-center relative">
                      <div className="text-3xl font-[1000]">{match.match_percentage}%</div>
                      <svg className="absolute -inset-[6px] w-24 h-24 -rotate-90">
                        <circle 
                          cx="48" cy="48" r="42" 
                          fill="transparent" 
                          stroke="currentColor" 
                          strokeWidth="6"
                          className="text-sky-400"
                          strokeDasharray={264}
                          strokeDashoffset={264 - (264 * match.match_percentage) / 100}
                          strokeLinecap="round"
                        />
                      </svg>
                    </div>
                  </div>
                </div>
                {/* Background Pattern */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-sky-400/10 blur-3xl -mr-20 -mt-20 rounded-full" />
              </motion.div>
            )}

            <section className="space-y-6">
              <h2 className="text-xl font-[900] text-sky-950 flex items-center gap-3">
                <div className="w-1.5 h-6 bg-sky-600 rounded-full" />
                Deskripsi Pekerjaan
              </h2>
              <div className="text-[16px] leading-relaxed text-slate-600 whitespace-pre-line bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
                {vacancy.description}
              </div>
            </section>

            <section className="space-y-6">
              <h2 className="text-xl font-[900] text-sky-950 flex items-center gap-3">
                <div className="w-1.5 h-6 bg-sky-600 rounded-full" />
                Kualifikasi & Skill
              </h2>
              <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm space-y-8">
                <div className="flex flex-wrap gap-2">
                  {vacancy.skills?.length > 0 ? vacancy.skills.map((skill) => (
                    <span key={skill.skill_id} className="flex items-center gap-2 bg-slate-50 text-slate-700 px-4 py-2.5 rounded-2xl text-[13px] font-bold border border-slate-100">
                      <PiCheckCircleFill className="text-emerald-500" size={18} />
                      {skill.skill_name}
                      {skill.is_mandatory && <span className="text-[10px] text-red-400 font-black ml-1 uppercase">Wajib</span>}
                    </span>
                  )) : (
                    <div className="py-4 text-slate-400 font-medium italic">Requirement skill belum ditambahkan.</div>
                  )}
                </div>
              </div>
            </section>
          </div>

          {/* Right Column: Sidebar */}
          <aside className="space-y-6">
            <div className="bg-white rounded-[32px] p-8 border border-slate-100 shadow-xl shadow-sky-950/[0.02] sticky top-24">
              <h3 className="text-lg font-[900] text-sky-950 mb-8 tracking-tight">Detail Informasi</h3>
              
              <div className="space-y-8">
                <div className="flex gap-4">
                  <div className="w-12 h-12 bg-sky-50 rounded-2xl flex items-center justify-center text-sky-600 shrink-0">
                    <PiClock size={24} />
                  </div>
                  <div>
                    <div className="text-[11px] font-extrabold text-slate-400 uppercase tracking-widest mb-1">Status</div>
                    <div className="text-sm font-bold text-sky-950">Penuh Waktu</div>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="w-12 h-12 bg-sky-50 rounded-2xl flex items-center justify-center text-sky-600 shrink-0">
                    <PiBriefcase size={24} />
                  </div>
                  <div>
                    <div className="text-[11px] font-extrabold text-slate-400 uppercase tracking-widest mb-1">Kompensasi</div>
                    <div className="text-sm font-bold text-sky-950">{displayPayment(vacancy.payment_type)}</div>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="w-12 h-12 bg-sky-50 rounded-2xl flex items-center justify-center text-sky-600 shrink-0">
                    <PiCalendarBlank size={24} />
                  </div>
                  <div>
                    <div className="text-[11px] font-extrabold text-slate-400 uppercase tracking-widest mb-1">Batas Lamaran</div>
                    <div className="text-sm font-bold text-sky-950">
                      {vacancy.close_date ? format(new Date(vacancy.close_date), 'dd MMMM yyyy') : '-'}
                    </div>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="w-12 h-12 bg-sky-50 rounded-2xl flex items-center justify-center text-sky-600 shrink-0">
                    <PiGlobe size={24} />
                  </div>
                  <div>
                    <div className="text-[11px] font-extrabold text-slate-400 uppercase tracking-widest mb-1">Website</div>
                    <a href={vacancy.company?.website_url || "#"} target="_blank" rel="noreferrer" className="text-sm font-bold text-sky-600 hover:underline">
                      Kunjungi Situs Web
                    </a>
                  </div>
                </div>
              </div>

              <div className="mt-12 pt-8 border-t border-slate-50">
                <p className="text-[12px] font-medium text-slate-400 leading-relaxed">
                  Pastikan Anda telah melengkapi profil dan CV sebelum menekan tombol Lamar Sekarang untuk hasil yang maksimal.
                </p>
              </div>
            </div>
          </aside>
        </div>
      </main>
    </div>
  );
}
