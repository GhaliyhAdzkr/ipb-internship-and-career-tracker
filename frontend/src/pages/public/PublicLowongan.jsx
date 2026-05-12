import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { 
  PiMagnifyingGlass, 
  PiMapPin, 
  PiBriefcase, 
  PiCaretDown,
  PiCheckCircleFill,
  PiArrowRightBold,
  PiLeaf,
  PiTerminal,
  PiMegaphone,
  PiFlask,
  PiMonitor,
  PiChartBar,
  PiCaretLeft,
  PiCaretRight,
  PiXCircle
} from 'react-icons/pi';
import { vacancyService } from '../../services/vacancyService';

export default function PublicLowongan() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  
  // Sync state with URL params
  const [searchQuery, setSearchQuery] = useState(searchParams.get('query') || '');
  const [location, setLocation] = useState(searchParams.get('location') || '');
  const [type, setType] = useState(searchParams.get('type') || '');
  const [industry, setIndustry] = useState(searchParams.get('industry') || '');
  const [academicLevel, setAcademicLevel] = useState(searchParams.get('academic') || '');
  const [currentPage, setCurrentPage] = useState(Number(searchParams.get('page')) || 1);
  const itemsPerPage = 6;

  // Update URL when filters change
  useEffect(() => {
    const params = {};
    if (searchQuery) params.query = searchQuery;
    if (location) params.location = location;
    if (type) params.type = type;
    if (industry) params.industry = industry;
    if (academicLevel) params.academic = academicLevel;
    if (currentPage > 1) params.page = currentPage;
    setSearchParams(params, { replace: true });
  }, [searchQuery, location, type, industry, academicLevel, currentPage]);

  const { data: vacanciesData, isLoading, isError, error } = useQuery({
    queryKey: ['public-vacancies', currentPage, searchQuery, location, type, industry, academicLevel],
    queryFn: () => vacancyService.getVacancies({ 
      page: currentPage, 
      perPage: itemsPerPage,
      query: searchQuery || undefined,
      location: location || undefined,
      type: type || undefined,
      industry: industry || undefined
      // academicLevel is UI-only for now as backend doesn't support it yet
    }),
  });

  const handleReset = () => {
    setSearchQuery('');
    setLocation('');
    setType('');
    setIndustry('');
    setAcademicLevel('');
    setCurrentPage(1);
  };

  const displayType = (value) => {
    const types = {
      'INTERNSHIP_GENERAL': 'Magang Umum',
      'MBKM_INTERNSHIP': 'Magang MBKM',
      'MBKM_STUDY_INDEPENDENT': 'MBKM Studi Independen',
      'FULL_TIME': 'Full Time'
    };
    return types[value] || value || '-';
  };

  const getIcon = (category, index) => {
    if (category?.toLowerCase().includes('sustainability')) return <PiLeaf size={24} />;
    if (category?.toLowerCase().includes('data') || category?.toLowerCase().includes('science')) return <PiTerminal size={24} />;
    if (category?.toLowerCase().includes('marketing')) return <PiMegaphone size={24} />;
    if (category?.toLowerCase().includes('research') || category?.toLowerCase().includes('food')) return <PiFlask size={24} />;
    
    // Fallback based on index for variety
    const icons = [<PiChartBar size={24} />, <PiMonitor size={24} />, <PiBriefcase size={24} />];
    return icons[index % 3];
  };

  const totalItems = vacanciesData?.total || 0;
  const totalPages = vacanciesData?.total_pages || 1;

  return (
    <div className="font-jakarta text-sky-950 bg-[#F8F9FF] min-h-screen">
      {/* Navbar */}
      <nav className="bg-white border-b border-slate-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-12">
            <Link to="/" className="flex items-center gap-2">
              <img src="/logo/laras.png" alt="LARAS" className="w-10 h-10 object-contain" />
              <span className="text-xl font-[900] tracking-tight">LARAS</span>
            </Link>
            <div className="hidden md:flex items-center gap-8 text-[15px]">
              <Link to="/" className="font-medium text-slate-500 hover:text-sky-900 transition-colors">Beranda</Link>
              <Link to="/lowongan" className="font-semibold text-sky-900 relative after:content-[''] after:absolute after:-bottom-1 after:left-0 after:w-full after:h-0.5 after:bg-sky-600">Lowongan</Link>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden lg:flex items-center bg-sky-50/50 border border-sky-100/50 rounded-full px-4 py-2 w-72 group focus-within:ring-2 focus-within:ring-sky-200 transition-all">
              <PiMagnifyingGlass className="text-slate-400 group-focus-within:text-sky-600" size={18} />
              <input
                className="bg-transparent border-none text-sm outline-none px-3 w-full text-sky-950 font-bold placeholder:text-slate-400 placeholder:font-bold"
                placeholder="Cari lowongan..."
              />
            </div>
            <Link to="/login" className="text-sm font-semibold text-sky-900 hover:text-sky-600 transition-colors">Masuk</Link>
            <Link to="/registration" className="bg-sky-950 text-white px-6 py-2.5 rounded-lg text-sm font-bold shadow-lg shadow-sky-900/10 hover:bg-sky-900 transition-all active:scale-95">Daftar</Link>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Header Section */}
        <section className="mb-12">
          <h1 className="text-4xl font-[900] text-sky-950 mb-3 tracking-tight">Eksplorasi Karirmu</h1>
          <p className="text-[15px] font-medium text-slate-500 max-w-2xl leading-relaxed">
            Temukan peluang magang dan karir profesional yang telah dikurasi khusus untuk mahasiswa dan alumni IPB University.
          </p>
        </section>

        {/* Search Bar Section */}
        <section className="bg-white rounded-2xl p-3 shadow-xl shadow-sky-900/5 border border-slate-100 mb-12">
          <div className="flex flex-col md:flex-row gap-3">
            <div className="flex-[2] flex items-center gap-3 px-4 py-3 bg-slate-50/50 rounded-xl border border-slate-100">
              <PiBriefcase className="text-slate-400" size={22} />
              <input 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Posisi, kata kunci, atau perusahaan..." 
                className="bg-transparent border-none outline-none w-full text-[15px] font-medium placeholder:text-slate-400" 
              />
            </div>
            <div className="flex-1 flex items-center gap-3 px-4 py-3 bg-slate-50/50 rounded-xl border border-slate-100">
              <PiMapPin className="text-slate-400" size={22} />
              <input 
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="Lokasi..." 
                className="bg-transparent border-none outline-none w-full text-[15px] font-medium placeholder:text-slate-400" 
              />
            </div>
            <div className="flex-1 flex items-center gap-3 px-4 py-3 bg-slate-50/50 rounded-xl border border-slate-100 relative">
              <PiBriefcase className="text-slate-400" size={22} />
              <select 
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="bg-transparent border-none outline-none w-full text-[15px] font-medium text-slate-600 appearance-none cursor-pointer"
              >
                <option value="">Semua Tipe</option>
                <option value="INTERNSHIP_GENERAL">Magang Umum</option>
                <option value="MBKM_INTERNSHIP">Magang MBKM</option>
                <option value="MBKM_STUDY_INDEPENDENT">Studi Independen</option>
                <option value="FULL_TIME">Full Time</option>
              </select>
              <PiCaretDown className="absolute right-4 text-slate-400 pointer-events-none" />
            </div>
          </div>
          
          <div className="mt-4 flex items-center gap-3 px-2 text-[13px]">
            <span className="text-slate-400 font-medium tracking-tight">Pencarian Populer:</span>
            <div className="flex gap-2">
              {['Data Analyst', 'Agronomi', 'Marketing'].map((tag) => (
                <button 
                  key={tag} 
                  onClick={() => setSearchQuery(tag)}
                  className="bg-sky-50 text-sky-700 font-bold px-3 py-1 rounded-full hover:bg-sky-100 transition-colors"
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>
        </section>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Filter */}
          <aside className="lg:w-72 shrink-0">
            <div className="bg-white rounded-2xl p-6 shadow-xl shadow-sky-900/5 border border-slate-100 sticky top-28">
              <div className="flex items-center justify-between mb-8">
                <h3 className="font-[900] text-sky-950 tracking-tight">Filter Detail</h3>
                <button 
                  onClick={handleReset}
                  className="text-[13px] font-bold text-sky-600 hover:underline flex items-center gap-1"
                >
                  <PiXCircle size={16} />
                  Reset
                </button>
              </div>

              <div className="space-y-8">
                <div>
                  <h4 className="text-[11px] font-[900] text-slate-400 uppercase tracking-widest mb-4">Bidang Industri</h4>
                  <div className="space-y-3">
                    <label className="flex items-center gap-3 cursor-pointer group">
                      <input 
                        type="checkbox" 
                        checked={industry === ''} 
                        onChange={() => setIndustry('')}
                        className="w-5 h-5 rounded border-slate-200 text-sky-600 focus:ring-sky-600" 
                      />
                      <span className={`text-sm font-bold ${industry === '' ? 'text-sky-950' : 'text-slate-600'} group-hover:text-sky-950 transition-colors`}>Semua Industri</span>
                    </label>
                    {['Agrikultur', 'Teknologi Informasi', 'FMCG', 'Perbankan'].map((label) => (
                      <label key={label} className="flex items-center gap-3 cursor-pointer group">
                        <input 
                          type="checkbox" 
                          checked={industry === label}
                          onChange={() => setIndustry(label)}
                          className="w-5 h-5 rounded border-slate-200 text-sky-600 focus:ring-sky-600" 
                        />
                        <span className={`text-sm font-bold ${industry === label ? 'text-sky-950' : 'text-slate-600'} group-hover:text-sky-950 transition-colors`}>{label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-[11px] font-[900] text-slate-400 uppercase tracking-widest mb-4">Kualifikasi Akademik</h4>
                  <div className="space-y-3">
                    <label className="flex items-center gap-3 cursor-pointer group">
                      <input 
                        type="radio" 
                        name="academic" 
                        checked={academicLevel === ''} 
                        onChange={() => setAcademicLevel('')}
                        className="w-5 h-5 border-slate-200 text-sky-600 focus:ring-sky-600" 
                      />
                      <span className={`text-sm font-bold ${academicLevel === '' ? 'text-sky-950' : 'text-slate-600'} group-hover:text-sky-950 transition-colors`}>Semua Tingkat</span>
                    </label>
                    {['Mahasiswa Aktif', 'Fresh Graduate'].map((label) => (
                      <label key={label} className="flex items-center gap-3 cursor-pointer group">
                        <input 
                          type="radio" 
                          name="academic" 
                          checked={academicLevel === label}
                          onChange={() => setAcademicLevel(label)}
                          className="w-5 h-5 border-slate-200 text-sky-600 focus:ring-sky-600" 
                        />
                        <span className={`text-sm font-bold ${academicLevel === label ? 'text-sky-950' : 'text-slate-600'} group-hover:text-sky-950 transition-colors`}>{label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </aside>

          {/* Listing Content */}
          <div className="flex-1">
            <div className="flex items-center justify-between mb-8">
              <span className="text-[14px] font-bold text-slate-400">
                Menampilkan <span className="text-sky-950">{totalItems}</span> lowongan
              </span>
              <div className="flex items-center gap-3">
                <span className="text-[13px] font-medium text-slate-400">Urutkan:</span>
                <button className="flex items-center gap-2 text-[13px] font-bold text-sky-950 bg-white px-3 py-1.5 rounded-lg border border-slate-100 shadow-sm">
                  <span>Terbaru</span>
                  <PiCaretDown size={14} />
                </button>
              </div>
            </div>

            {/* Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              {isLoading ? (
                [1,2,3,4].map(i => (
                  <div key={i} className="h-[280px] bg-white rounded-2xl animate-pulse border border-slate-100 shadow-sm" />
                ))
              ) : isError ? (
                <div className="col-span-full py-20 text-center text-red-500 font-bold bg-white rounded-2xl border border-red-50">
                  Gagal memuat lowongan: {error.message}
                </div>
              ) : (
                vacanciesData?.items?.map((item, index) => (
                  <VacancyCard 
                    key={item.id}
                    id={item.id}
                    title={item.title}
                    company={item.company?.name || 'Perusahaan'}
                    companyLogo={item.company?.logo_url}
                    location={item.location}
                    type={displayType(item.type)}
                    deadline={item.close_date ? format(new Date(item.close_date), 'dd MMM yyyy') : 'N/A'}
                    icon={getIcon(item.title, index)}
                  />
                ))
              )}
              {!isLoading && totalItems === 0 && (
                <div className="col-span-full py-20 text-center text-slate-400 font-bold bg-white rounded-2xl border border-dashed border-slate-200">
                  Tidak ada lowongan ditemukan.
                </div>
              )}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-16 flex items-center justify-center gap-3">
                <button 
                  disabled={currentPage === 1}
                  onClick={() => setCurrentPage(prev => prev - 1)}
                  className="w-10 h-10 rounded-xl bg-white border border-slate-100 flex items-center justify-center text-slate-400 hover:text-sky-600 disabled:opacity-30 transition-all shadow-sm"
                >
                  <PiCaretLeft size={20} weight="bold" />
                </button>
                <div className="flex items-center gap-2">
                  {[...Array(totalPages)].map((_, i) => (
                    <button 
                      key={i}
                      onClick={() => setCurrentPage(i + 1)}
                      className={`w-10 h-10 rounded-xl font-[900] text-sm transition-all shadow-sm ${
                        currentPage === i + 1 
                          ? 'bg-sky-950 text-white shadow-sky-950/20' 
                          : 'bg-white text-slate-400 hover:text-sky-950 border border-slate-100'
                      }`}
                    >
                      {i + 1}
                    </button>
                  ))}
                </div>
                <button 
                  disabled={currentPage === totalPages}
                  onClick={() => setCurrentPage(prev => prev + 1)}
                  className="w-10 h-10 rounded-xl bg-white border border-slate-100 flex items-center justify-center text-slate-400 hover:text-sky-600 disabled:opacity-30 transition-all shadow-sm"
                >
                  <PiCaretRight size={20} weight="bold" />
                </button>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white pt-24 pb-12 border-t border-slate-100 mt-20">
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

function VacancyCard({ id, title, company, companyLogo, location, type, deadline, icon }) {
  const [imgError, setImgError] = React.useState(false);

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-xl shadow-sky-900/[0.03] flex flex-col group hover:shadow-sky-900/10 transition-all duration-300">
      <div className="flex justify-between items-start mb-6">
        <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center text-sky-600 border border-slate-100 overflow-hidden group-hover:border-sky-100 transition-colors p-1.5">
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
        <h3 className="text-[17px] font-[900] text-sky-950 mb-1 group-hover:text-sky-600 transition-colors line-clamp-1">{title}</h3>
        <p className="text-[14px] font-medium text-slate-400 mb-6">{company}</p>
        
        <div className="flex flex-wrap gap-2">
          <span className="bg-slate-50 text-slate-500 text-[11px] font-bold px-3 py-1.5 rounded-lg flex items-center gap-1.5">
            <PiMapPin size={14} />
            {location}
          </span>
          <span className="bg-slate-50 text-slate-500 text-[11px] font-bold px-3 py-1.5 rounded-lg flex items-center gap-1.5">
            <PiBriefcase size={14} />
            {type}
          </span>
        </div>
      </div>
      
      <div className="pt-6 border-t border-slate-50 flex items-center justify-between mt-auto">
        <span className="text-[12px] font-bold text-slate-400 tracking-tight">Ditutup: {deadline}</span>
        <Link to={`/detail/${id}`} className="flex items-center gap-1.5 text-[13px] font-[900] text-sky-950 group-hover:text-sky-600 transition-colors">
          <span>Detail</span>
          <PiArrowRightBold size={14} />
        </Link>
      </div>
    </div>
  );
}
