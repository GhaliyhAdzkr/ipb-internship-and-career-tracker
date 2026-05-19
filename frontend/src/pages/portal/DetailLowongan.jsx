import { useNavigate, useParams, Link } from "react-router-dom";
 
import { motion } from "framer-motion";
import { format } from 'date-fns';
import { useApplications } from "../../hooks/useApplications";
import { useVacancyDetail } from "../../hooks/useVacancyDetail";
import toast from "react-hot-toast";
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
  PiXCircle
} from "react-icons/pi";
import { resolveBackendAssetUrl } from "../../utils/assetUrl";

export default function DetailLowongan() {
  const navigate = useNavigate();
  const { vacancyId } = useParams();
  const token = localStorage.getItem('token');
  const { apply, isApplying } = useApplications({ enabled: false });
  const {
    vacancy,
    isLoadingVacancy,
    isErrorVacancy,
    isWishlisted,
    toggleWishlistMutation,
    jobMatch
  } = useVacancyDetail(vacancyId, token);

  const handleApply = async () => {
    if (!token) {
      navigate("/login");
      return;
    }
    
    try {
      await apply({ vacancy_id: vacancyId });
      toast.success("Lamaran berhasil dikirim!");
      
      // If there is an external source URL, open it in a new tab
      if (vacancy?.source_url) {
        window.open(vacancy.source_url, "_blank", "noreferrer");
      }
      
      // Redirect to the applications tracking board
      navigate("/app/lamaran");
    } catch (error) {
      console.error("Failed to apply:", error);
      toast.error(error.response?.data?.detail || "Gagal melamar lowongan.");
    }
  };

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

  if (isLoadingVacancy) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="flex flex-col items-center gap-4">
          <PiSpinnerGap size={48} className="animate-spin text-sky-600" />
          <p className="text-sm font-bold text-sky-950/40 uppercase tracking-[0.2em]">Memuat Detail...</p>
        </div>
      </div>
    );
  }

  if (isErrorVacancy || !vacancy) {
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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
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
                LARAS
              </span>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="relative bg-white border-b border-slate-100 pt-12 pb-16 overflow-hidden">
        {/* Decorative Background */}
        <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-sky-50/50 to-transparent pointer-events-none" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 relative z-10">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
            <div className="flex flex-col sm:flex-row gap-5 sm:gap-6 items-start md:items-center">
              <motion.div 
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                className="w-20 h-20 md:w-24 md:h-24 bg-white rounded-[28px] border border-slate-100 shadow-xl shadow-sky-900/5 flex items-center justify-center p-4 shrink-0 overflow-hidden"
              >
                {vacancy.company?.logo_url ? (
                  <img 
                    src={resolveBackendAssetUrl(vacancy.company.logo_url)} 
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
                  className="text-2xl sm:text-3xl md:text-4xl font-[1000] text-sky-950 mb-2 tracking-tight"
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
              <button 
                onClick={() => {
                  if (!token) {
                    navigate("/login");
                    return;
                  }
                  toggleWishlistMutation.mutate();
                }}
                disabled={toggleWishlistMutation.isPending}
                className={`px-6 py-4 rounded-2xl font-bold flex items-center justify-center gap-2 transition-all active:scale-95 border ${
                  isWishlisted 
                    ? "bg-amber-50 text-amber-600 border-amber-200 hover:bg-amber-100/80" 
                    : "bg-white text-sky-950 border-slate-200 hover:bg-slate-50"
                }`}
              >
                <PiBookmarkSimple size={22} weight={isWishlisted ? "fill" : "regular"} />
                <span>{isWishlisted ? "Tersimpan" : "Simpan"}</span>
              </button>
              
              <button 
                onClick={handleApply}
                disabled={isApplying}
                className="bg-sky-950 text-white px-10 py-4 rounded-2xl font-bold flex items-center justify-center gap-2 hover:bg-sky-900 transition-all active:scale-95 shadow-xl shadow-sky-900/20 disabled:opacity-70"
              >
                {isApplying ? (
                  <PiSpinnerGap size={20} className="animate-spin text-white" />
                ) : (
                  <>
                    <span>Lamar Sekarang</span>
                    <PiCaretRightBold size={18} />
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 mt-10 sm:mt-12">
        <div className="grid lg:grid-cols-3 gap-8 sm:gap-12">
          {/* Left Column: Details */}
          <div className="lg:col-span-2 space-y-8 sm:space-y-12">

            <section className="space-y-6">
              <h2 className="text-xl font-[900] text-sky-950 flex items-center gap-3">
                <div className="w-1.5 h-6 bg-sky-600 rounded-full" />
                Deskripsi Pekerjaan
              </h2>
              <div className="text-[15px] sm:text-[16px] leading-relaxed text-slate-600 whitespace-pre-line bg-white rounded-3xl p-5 sm:p-8 border border-slate-100 shadow-sm">
                {vacancy.description}
              </div>
            </section>

            <section className="space-y-6">
              <h2 className="text-xl font-[900] text-sky-950 flex items-center gap-3">
                <div className="w-1.5 h-6 bg-sky-600 rounded-full" />
                Kualifikasi & Skill
              </h2>
              <div className="bg-white rounded-3xl p-5 sm:p-8 border border-slate-100 shadow-sm space-y-8">
                <div className="flex flex-wrap gap-2">
                  {vacancy.skills?.length > 0 ? vacancy.skills.map((skill) => (
                    <span key={skill.skill_id} className="flex items-center gap-2 bg-sky-50/50 text-sky-950 px-4 py-2.5 rounded-2xl text-[13px] font-bold border border-sky-100/50">
                      <PiCheckCircleFill className="text-sky-600" size={18} />
                      {skill.skill_name}
                      {skill.is_mandatory && <span className="text-[10px] text-sky-700 bg-sky-100 px-2 py-0.5 rounded border border-sky-200/50 font-black ml-1 uppercase">Wajib</span>}
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
            {/* Case 1: Token exists but student hasn't uploaded their CV (jobMatch has null match_percentage or !jobMatch) */}
            {token && (!jobMatch || jobMatch.match_percentage === null) && (
              <div className="bg-white rounded-[32px] p-5 sm:p-8 border border-slate-100 shadow-xl shadow-sky-950/[0.02]">
                <h3 className="text-lg font-[900] text-sky-950 mb-6 tracking-tight">Kesesuaian Profil</h3>
                <p className="text-[13px] text-slate-500 leading-relaxed font-medium mb-6">
                  Sistem dapat menganalisis kesesuaian keahlian Anda dengan lowongan ini secara otomatis. Unggah CV di profil Anda untuk memulai!
                </p>
                <Link 
                  to="/app/profil" 
                  className="inline-flex w-full py-3 bg-sky-600 hover:bg-sky-700 text-white rounded-2xl text-xs font-bold items-center justify-center transition-all active:scale-95 shadow-md shadow-sky-600/10"
                >
                  Unggah CV Sekarang
                </Link>
              </div>
            )}

            {/* Case 2: Token exists, CV uploaded, but vacancy has no skill requirements */}
            {token && jobMatch && jobMatch.match_percentage !== null && jobMatch.total_required_skills === 0 && (
              <div className="bg-white rounded-[32px] p-5 sm:p-8 border border-slate-100 shadow-xl shadow-sky-950/[0.02]">
                <h3 className="text-lg font-[900] text-sky-950 mb-6 tracking-tight">Kesesuaian Profil</h3>
                <p className="text-[13px] text-slate-500 leading-relaxed font-medium">
                  Lowongan ini belum memuat kualifikasi keahlian khusus secara spesifik di sistem, sehingga analisis kesesuaian tidak dapat dihitung.
                </p>
              </div>
            )}

            {/* Case 3: Token exists, CV uploaded, and vacancy has skill requirements */}
            {token && jobMatch && jobMatch.match_percentage !== null && jobMatch.total_required_skills > 0 && (
              <div className="bg-white rounded-[32px] p-5 sm:p-8 border border-slate-100 shadow-xl shadow-sky-950/[0.02]">
                <div className="flex items-center justify-between mb-8">
                  <h3 className="text-lg font-[900] text-sky-950 tracking-tight">Kesesuaian Profil</h3>
                  <span className="text-[10px] bg-sky-50 text-sky-700 font-bold px-2 py-0.5 rounded-full border border-sky-100/50 flex items-center gap-0.5">
                    Aktif
                  </span>
                </div>

                <div className="space-y-6">
                  <div className="space-y-3">
                    <div className="flex justify-between items-baseline">
                      <span className="text-[11px] font-extrabold text-slate-400 uppercase tracking-widest">Kecocokan</span>
                      <span className="text-3xl font-[900] text-sky-950 tracking-tight">{Math.round(jobMatch.match_percentage)}%</span>
                    </div>
                    {/* Progress Bar */}
                    <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-sky-600 rounded-full transition-all duration-1000"
                        style={{ width: `${jobMatch.match_percentage}%` }}
                      />
                    </div>
                  </div>

                  <div className="space-y-4 pt-6 border-t border-slate-100 text-[13px]">
                    <div className="flex flex-col gap-3">
                      <span className="text-slate-400 font-extrabold text-[11px] uppercase tracking-widest">Skill yang cocok</span>
                      <div className="flex flex-wrap gap-2">
                        {jobMatch.matched_skills.length > 0 ? (
                          jobMatch.matched_skills.map((skill) => (
                            <span key={skill} className="flex items-center gap-1.5 bg-sky-50/50 text-sky-950 px-3 py-1.5 rounded-2xl text-[12px] font-bold border border-sky-100/50">
                              <PiCheckCircleFill className="text-sky-600" size={16} />
                              {skill}
                            </span>
                          ))
                        ) : (
                          <span className="text-slate-400 italic text-xs font-medium">Belum ada skill yang cocok</span>
                        )}
                      </div>
                    </div>

                    {jobMatch.missing_mandatory_skills.length > 0 && (
                      <div className="flex flex-col gap-3 pt-3">
                        <span className="text-slate-400 font-extrabold text-[11px] uppercase tracking-widest">Skill wajib belum dimiliki</span>
                        <div className="flex flex-wrap gap-2">
                          {jobMatch.missing_mandatory_skills.map((skill) => (
                            <span key={skill} className="flex items-center gap-1.5 bg-slate-50 text-slate-500 px-3 py-1.5 rounded-2xl text-[12px] font-medium border border-slate-100/80">
                              <PiXCircle className="text-slate-400" size={16} />
                              {skill}
                              <span className="text-[9px] text-sky-700 bg-sky-100 px-1.5 py-0.5 rounded border border-sky-200/50 font-black ml-1 uppercase">Wajib</span>
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="mt-6 pt-6 border-t border-slate-50">
                    <p className="text-[12px] font-medium text-slate-400 leading-relaxed">
                      Analisis keahlian ini bersifat informatif untuk membantu Anda mempersiapkan diri. Anda tetap dapat melamar lowongan ini meskipun skor kecocokan belum maksimal.
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div className="bg-white rounded-[32px] p-5 sm:p-8 border border-slate-100 shadow-xl shadow-sky-950/[0.02] lg:sticky lg:top-24">
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
