import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { format } from 'date-fns';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay } from 'swiper/modules'; 
import { useLandingVacancies } from '../../hooks/useVacancies';
import { useAuth } from '../../hooks/useAuth';
import PARTNERS from '../../data/partners.json';
import { motion, AnimatePresence } from 'framer-motion';
import 'swiper/css';

import { 
  PiMagnifyingGlass, 
  PiBriefcase, 
  PiMapPin, 
  PiCheckCircleFill,
  PiArrowRightBold,
  PiMonitor,
  PiChartBar,
  PiMegaphone,
  PiBuildings,
  PiCursorClickFill
} from 'react-icons/pi';

export default function Landing() {
  const navigate = useNavigate();
  const { data: vacanciesData, isLoading, isError, error } = useLandingVacancies();
  const { user } = useAuth();

  // Log for debugging purposes
  useEffect(() => {
    if (vacanciesData) {
      console.log('Vacancies Data:', vacanciesData);
    }
    if (error) {
      console.error('Vacancies Fetch Error:', error);
    }
  }, [vacanciesData, error]);

  const displayType = (value) => {
    switch (value) {
      case 'INTERNSHIP_GENERAL': return 'Magang Umum';
      case 'MBKM_INTERNSHIP': return 'MBKM Magang';
      case 'MBKM_STUDY_INDEPENDENT': return 'MBKM Studi Independen';
      case 'FULL_TIME': return 'Full Time';
      default: return value || '-';
    }
  };

  return (
    <div className="font-jakarta text-sky-950 bg-white min-h-screen">
      {/* Navbar */}
      <nav className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-slate-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-12">
            <Link to="/" className="flex items-center gap-2">
              <img src="/logo/laras.png" alt="LARAS" className="w-10 h-10 object-contain" />
              <span className="text-xl font-[900] tracking-tight">LARAS</span>
            </Link>
            <div className="hidden md:flex items-center gap-8 text-[15px]">
              <Link to="/" className="font-semibold text-sky-900 relative after:content-[''] after:absolute after:-bottom-1 after:left-0 after:w-full after:h-0.5 after:bg-sky-600">Beranda</Link>
              <Link to="/lowongan" className="font-medium text-slate-500 hover:text-sky-900 transition-colors">Lowongan</Link>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden lg:flex items-center bg-sky-50/50 border border-sky-100/50 rounded-full px-4 py-2 w-72 group focus-within:ring-2 focus-within:ring-sky-200 transition-all">
              <PiMagnifyingGlass className="text-slate-400 group-focus-within:text-sky-600" size={18} />
              <input
                aria-label="search"
                className="bg-transparent border-none text-sm outline-none px-3 w-full text-sky-950 font-bold placeholder:text-slate-400 placeholder:font-bold"
                placeholder="Cari lowongan..."
              />
            </div>
            {user ? (
              <Link 
                to={user.role === 'ADMIN' ? '/app/admin/dashboard' : '/app/home'} 
                className="bg-sky-950 text-white px-6 py-2.5 rounded-lg text-sm font-bold shadow-lg shadow-sky-900/10 hover:bg-sky-900 transition-all active:scale-95"
              >
                Dashboard
              </Link>
            ) : (
              <>
                <Link to="/login" className="text-sm font-semibold text-sky-900 hover:text-sky-600 transition-colors">Masuk</Link>
                <Link to="/registration" className="bg-sky-950 text-white px-6 py-2.5 rounded-lg text-sm font-bold shadow-lg shadow-sky-900/10 hover:bg-sky-900 transition-all active:scale-95">Daftar</Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="relative min-h-[640px] flex items-center overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img 
            src="/assets/hero-campus.jpg" 
            alt="Campus Background" 
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-white via-white/90 to-white/40"></div>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 py-20 w-full">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="max-w-xl">
              <div className="inline-flex items-center bg-sky-50 border border-sky-100 rounded-full px-4 py-1.5 mb-6">
                <span className="text-[13px] font-bold text-sky-700 tracking-wide">Portal Resmi IPB University</span>
              </div>
              
              <h1 className="text-5xl md:text-6xl font-[900] leading-[1.1] text-sky-950 mb-6">
                Bangun Karier <br />
                <span className="text-sky-600">Profesional</span> Anda
              </h1>
              
              <p className="text-[17px] leading-relaxed text-slate-600 mb-10 font-medium">
                Platform magang dan rekrutmen terintegrasi untuk mahasiswa dan alumni IPB University. Temukan peluang dari mitra industri terbaik.
              </p>

              {/* Search Box */}
              <div className="bg-white rounded-2xl p-2 shadow-2xl shadow-sky-900/10 border border-slate-100 backdrop-blur-sm">
                <form 
                  onSubmit={(e) => {
                    e.preventDefault();
                    const query = e.target.query.value;
                    const location = e.target.location.value;
                    navigate(`/lowongan?query=${query}&location=${location}`);
                  }}
                  className="flex flex-col md:flex-row gap-2"
                >
                  <div className="flex-1 flex items-center gap-3 px-4 py-3 bg-sky-50/30 rounded-xl">
                    <PiBriefcase className="text-sky-400" size={22} />
                    <input 
                      name="query"
                      placeholder="Posisi atau perusahaan" 
                      className="bg-transparent border-none outline-none w-full text-[15px] font-medium placeholder:text-slate-400" 
                    />
                  </div>
                  <div className="md:w-40 flex items-center gap-3 px-4 py-3 bg-sky-50/30 rounded-xl border-l md:border-l-0 border-slate-100">
                    <PiMapPin className="text-sky-400" size={22} />
                    <input 
                      name="location"
                      placeholder="Lokasi" 
                      className="bg-transparent border-none outline-none w-full text-[15px] font-medium placeholder:text-slate-400" 
                    />
                  </div>
                  <button type="submit" className="bg-sky-950 text-white px-8 py-4 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-sky-900 transition-all active:scale-95 shadow-xl shadow-sky-900/20">
                    <PiMagnifyingGlass size={20} weight="bold" />
                    <span>Cari</span>
                  </button>
                </form>
              </div>
              
              <div className="mt-6 flex items-center gap-2 text-[13px]">
                <span className="text-slate-400 font-medium tracking-tight">Pencarian populer:</span>
                <div className="flex gap-2">
                  {['Data Analyst', 'Agronomi', 'Management Trainee'].map((item) => (
                    <button 
                      key={item} 
                      onClick={() => navigate(`/lowongan?query=${item}`)}
                      className="text-sky-700 font-bold hover:underline"
                    >
                      {item}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Decorative Element */}
            <div className="hidden lg:block relative">
              <div className="relative w-full h-[540px] flex items-center justify-end">
                {/* Main Card Mockup */}
                <motion.div 
                  initial={{ opacity: 0, y: 40 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, ease: "easeOut" }}
                  className="relative w-[420px] bg-white rounded-[32px] shadow-2xl shadow-sky-900/10 border border-slate-50 overflow-hidden z-10"
                >
                  <div className="p-8">
                    <div className="flex justify-between items-start mb-10">
                      <div className="w-14 h-14 bg-sky-50 rounded-2xl flex items-center justify-center">
                        <PiBriefcase className="text-sky-600" size={28} />
                      </div>
                      <span className="bg-sky-50 text-sky-700 text-[11px] font-[900] px-4 py-1.5 rounded-full uppercase tracking-wider">Baru</span>
                    </div>
                    
                    <div className="space-y-6">
                      <div className="h-7 bg-slate-100 rounded-full flex items-center px-4 w-[90%]">
                         <span className="text-[10px] font-bold text-slate-400">Management Trainee</span>
                      </div>
                      <div className="h-5 bg-slate-50 rounded-full flex items-center px-4 w-[70%]">
                        <span className="text-[8px] font-bold text-slate-300">PT Astra International Tbk.</span>
                      </div>
                      <div className="flex gap-2">
                        <div className="h-4 w-16 bg-sky-50/50 rounded-full" />
                        <div className="h-4 w-20 bg-sky-50/50 rounded-full" />
                      </div>
                    </div>

                    <div className="mt-12 pt-8 border-t border-slate-50 flex justify-between items-center">
                      <div className="w-24 h-3 bg-slate-100 rounded-full"></div>
                      <div className="bg-sky-950 text-white text-[10px] font-bold px-4 py-2 rounded-lg">Lamar Sekarang</div>
                    </div>
                  </div>

                  {/* Simulated Cursor Animation */}
                  <motion.div
                    animate={{
                      x: [100, 315, 315, 315, 315, 315],
                      y: [300, 360, 360, 360, 360, 360],
                      scale: [1, 1, 0.8, 1, 1, 1],
                      opacity: [0, 1, 1, 1, 1, 0]
                    }}
                    transition={{
                      duration: 6,
                      repeat: Infinity,
                      times: [0, 0.2, 0.25, 0.3, 0.8, 1],
                      repeatDelay: 1
                    }}
                    className="absolute z-30 text-sky-600 drop-shadow-xl"
                  >
                    <PiCursorClickFill size={32} />
                  </motion.div>
                </motion.div>

                {/* Kartu Status Alur Cerita */}
                <div className="absolute bottom-10 left-0 w-80 z-20 pointer-events-none">
                  <AnimatePresence>
                    {/* Tahap 1: Lamaran Terkirim */}
                    <motion.div 
                      key="submitted"
                      initial={{ opacity: 0, scale: 0.8, y: 20 }}
                      animate={{ 
                        opacity: [0, 1, 1, 0],
                        scale: [0.8, 1, 1, 0.8],
                        y: [20, 0, 0, -20]
                      }}
                      transition={{ 
                        duration: 6, 
                        repeat: Infinity,
                        times: [0, 0.28, 0.5, 0.55],
                        repeatDelay: 1
                      }}
                      className="absolute bottom-0 w-full bg-white rounded-2xl shadow-2xl shadow-sky-900/20 border border-slate-50 p-5 flex items-center gap-4"
                    >
                      <div className="w-12 h-12 bg-sky-100 rounded-full flex items-center justify-center text-sky-600 shrink-0">
                        <PiBriefcase size={28} />
                      </div>
                      <div>
                        <div className="text-sm font-[900] text-sky-950">Lamaran Terkirim</div>
                        <div className="text-[11px] font-bold text-slate-400 uppercase tracking-tighter">Menunggu Review HRD...</div>
                      </div>
                    </motion.div>

                    {/* Tahap 2: Lamaran Diterima */}
                    <motion.div 
                      key="accepted"
                      initial={{ opacity: 0, scale: 0.8, y: 20 }}
                      animate={{ 
                        opacity: [0, 0, 1, 1, 0],
                        scale: [0.8, 0.8, 1, 1, 0.8],
                        y: [20, 20, 0, 0, -20]
                      }}
                      transition={{ 
                        duration: 6, 
                        repeat: Infinity,
                        times: [0, 0.55, 0.6, 0.9, 1],
                        repeatDelay: 1
                      }}
                      className="absolute bottom-0 w-full bg-white rounded-2xl shadow-2xl shadow-sky-900/20 border border-slate-50 p-5 flex items-center gap-4"
                    >
                      <div className="w-12 h-12 bg-sky-500 rounded-full flex items-center justify-center text-white shrink-0">
                        <PiCheckCircleFill size={28} />
                      </div>
                      <div>
                        <div className="text-sm font-[900] text-sky-950">Lamaran Diterima</div>
                        <div className="text-[11px] font-bold text-slate-400 uppercase tracking-tighter">PT Astra International Tbk.</div>
                      </div>
                    </motion.div>
                  </AnimatePresence>
                </div>

                {/* Lingkaran Dekoratif Latar Belakang */}
                <motion.div 
                  animate={{ 
                    scale: [1, 1.1, 1],
                    opacity: [0.3, 0.5, 0.3]
                  }}
                  transition={{ duration: 8, repeat: Infinity }}
                  className="absolute top-10 right-10 w-64 h-64 bg-sky-100/50 rounded-full blur-3xl -z-0"
                />
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Bagian Partner Carousel Modern */}
      <section className="py-16 border-b border-slate-50 overflow-hidden">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-center text-[12px] font-extrabold text-slate-400 uppercase tracking-[0.2em] mb-12">
            Bergabung bersama perusahaan terbaik
          </h2>
          
          <div className="relative overflow-hidden px-4 md:px-0">
            {/* Fade Overlays */}
            <div className="absolute left-0 top-0 bottom-0 w-24 bg-gradient-to-r from-white to-transparent z-10 pointer-events-none" />
            <div className="absolute right-0 top-0 bottom-0 w-24 bg-gradient-to-l from-white to-transparent z-10 pointer-events-none" />
            
            <Swiper
              modules={[Autoplay]}
              spaceBetween={100}
              slidesPerView={2}
              loop={true}
              autoplay={{
                delay: 2000,
                disableOnInteraction: false,
              }}
              breakpoints={{
                640: { slidesPerView: 3 },
                1024: { slidesPerView: 5 },
              }}
              className="partner-swiper !py-8"
            >
              {PARTNERS.map((partner) => (
                <SwiperSlide key={partner.name}>
                  <div className="flex items-center justify-center">
                    <a 
                      href={partner.website} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="flex items-center justify-center h-12 w-full transition-all duration-300 cursor-pointer hover:scale-110 hover:z-50 relative group/logo"
                      title={partner.name}
                    >
                      <img 
                        src={partner.logo} 
                        alt={partner.alt} 
                        className="max-w-full max-h-full object-contain mx-auto" 
                        onError={(e) => {
                          e.target.style.display = 'none';
                          e.target.nextSibling.style.display = 'flex';
                        }}
                      />
                      <div className="hidden items-center gap-2 font-bold text-slate-300">
                        <PiBuildings size={20} />
                        <span className="text-xs">{partner.name}</span>
                      </div>
                    </a>
                  </div>
                </SwiperSlide>
              ))}
            </Swiper>
          </div>
        </div>
      </section>

      {/* Jobs Section */}
      <main className="max-w-7xl mx-auto px-6 py-24">
        <section>
          <div className="flex items-end justify-between mb-12">
            <div>
              <h2 className="text-3xl font-[900] text-sky-950 mb-3 tracking-tight">Temukan karir yang sesuai dengan anda</h2>
              <p className="text-[15px] font-medium text-slate-500">Rekomendasi lowongan magang terbaru untuk Anda</p>
            </div>
            <Link to="/lowongan" className="flex items-center gap-2 text-sky-950 font-[900] text-[15px] hover:text-sky-600 transition-colors group">
              <span>Lihat Semua</span>
              <PiArrowRightBold className="group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {isLoading ? (
              [1, 2, 3].map(i => (
                <div key={i} className="h-[320px] bg-slate-50 rounded-2xl animate-pulse border border-slate-100"></div>
              ))
            ) : isError ? (
              <div className="col-span-full p-6 bg-red-50 border border-red-100 rounded-2xl text-red-600 text-sm font-medium">
                Gagal memuat lowongan: {error.message || 'Koneksi ke server bermasalah'}
              </div>
            ) : (
              vacanciesData?.items?.map((item, index) => (
                <JobCard 
                  key={item.id}
                  id={item.id}
                  title={item.title}
                  company={item.company?.name || 'Perusahaan'}
                  companyLogo={item.company?.logo_url}
                  icon={index % 3 === 0 ? <PiChartBar size={24} /> : index % 3 === 1 ? <PiMonitor size={24} /> : <PiMegaphone size={24} />}
                  tags={[displayType(item.type), item.location]}
                  deadline={item.close_date ? format(new Date(item.close_date), 'dd MMM yyyy') : 'N/A'}
                />
              ))
            )}
            {!isLoading && !isError && (!vacanciesData?.items || vacanciesData.items.length === 0) && (
              <div className="col-span-full py-12 text-center text-slate-400 font-medium border border-dashed border-slate-200 rounded-2xl">
                Belum ada lowongan tersedia saat ini.
              </div>
            )}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white pt-24 pb-12 border-t border-slate-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-start gap-12 mb-16">
            <div className="max-w-xs">
              <Link to="/" className="flex items-center gap-2 mb-6">
                <img src="/logo/laras.png" alt="LARAS" className="w-8 h-8 object-contain" />
                <span className="text-xl font-[900] tracking-tight text-sky-950">LARAS</span>
              </Link>
              <p className="text-[13px] font-medium text-slate-400 leading-loose">
                © 2026 LARAS IPB University. Supported by CDA.
              </p>
            </div>
            
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-x-12 gap-y-8">
              <Link to="#" className="text-[13px] font-bold text-slate-500 hover:text-sky-900 transition-colors">Tentang LARAS</Link>
              <Link to="#" className="text-[13px] font-bold text-slate-500 hover:text-sky-900 transition-colors">Kebijakan Privasi</Link>
              <Link to="#" className="text-[13px] font-bold text-slate-500 hover:text-sky-900 transition-colors">Syarat & Ketentuan</Link>
              <Link to="#" className="text-[13px] font-bold text-slate-500 hover:text-sky-900 transition-colors">Pusat Bantuan</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function JobCard({ id, title, company, companyLogo, icon, tags, deadline }) {
  const [imgError, setImgError] = useState(false);

  return (
    <Link to={`/detail/${id}`} className="bg-white p-8 rounded-2xl border border-slate-100 shadow-xl shadow-sky-900/[0.03] flex flex-col group hover:shadow-sky-900/10 transition-all duration-300">
      <div className="flex justify-between items-start mb-6">
        <div className="w-14 h-14 bg-white rounded-2xl flex items-center justify-center text-sky-600 border border-slate-100 overflow-hidden group-hover:border-sky-100 transition-colors p-1.5">
          {companyLogo && !imgError ? (
            <img 
              src={companyLogo} 
              alt={company} 
              className="w-full h-auto max-h-full object-contain"
              onError={() => setImgError(true)}
              referrerPolicy="no-referrer"
            />
          ) : (
            <div className="w-full h-full bg-sky-50 flex items-center justify-center text-sky-600">
              {icon}
            </div>
          )}
        </div>
        <div className="bg-sky-50 border border-sky-100 text-sky-700 text-[10px] font-bold px-3 py-1 rounded-full flex items-center gap-1.5 uppercase tracking-wider">
          <PiCheckCircleFill size={14} />
          Dikurasi CDA
        </div>
      </div>
      
      <div className="flex-1 mb-8">
        <h3 className="text-lg font-[900] text-sky-950 mb-1 group-hover:text-sky-600 transition-colors line-clamp-2">{title}</h3>
        <p className="text-sm font-medium text-slate-400">{company}</p>
        
        <div className="flex flex-wrap gap-2 mt-4">
          {tags.filter(Boolean).map(tag => (
            <span key={tag} className="bg-slate-50 text-slate-500 text-[11px] font-bold px-3 py-1.5 rounded-lg border border-slate-100/50">
              {tag}
            </span>
          ))}
        </div>
      </div>
      
      <div className="pt-6 border-t border-slate-50 flex items-center justify-between mt-auto">
        <span className="text-[12px] font-bold text-slate-400 tracking-tight">Berakhir {deadline}</span>
        <span className="text-[13px] font-[900] text-sky-950 group-hover:text-sky-600 transition-colors">Detail Lowongan</span>
      </div>
    </Link>
  );
}
