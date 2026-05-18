import React, { useState } from "react";
import { 
    PiPlusBold, 
    PiMagnifyingGlassBold, 
    PiPencilSimpleBold, 
    PiTrashBold,
    PiBriefcaseThin,
    PiMapPinBold,
    PiBuildingsBold,
    PiGlobeSimpleBold,
    PiCheckCircleFill,
    PiXCircleFill,
    PiCloudArrowDownBold,
    PiFunnelBold,
    PiCaretDown,
    PiCalendarBold,
    PiSpinnerGap
} from "react-icons/pi";
import { useAdminVacancies } from "../../hooks/useAdminVacancies";
import vacancyService from "../../services/vacancyService";
import ConfirmModal from "../../components/ConfirmModal";

function AdminVacancies() {
    const [searchTerm, setSearchTerm] = useState("");
    const [activeTab, setActiveTab] = useState("all");
    const [typeFilter, setTypeFilter] = useState("all");
    const [statusFilter, setStatusFilter] = useState("all");
    const [industryFilter, setIndustryFilter] = useState("all");
    const [isConfirmOpen, setIsConfirmOpen] = useState(false);
    const [selectedVacancy, setSelectedVacancy] = useState(null);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [openSkillDropdownIndex, setOpenSkillDropdownIndex] = useState(null);
    const [skillSearchQuery, setSkillSearchQuery] = useState("");
    const [formData, setFormData] = useState({
        title: "",
        company_id: "",
        location: "",
        type: "INTERNSHIP_GENERAL",
        payment_type: "UNPAID",
        description: "",
        source_url: "",
        open_date: new Date().toISOString().split('T')[0],
        close_date: "",
        compensation_min: "",
        compensation_max: "",
        compensation_note: "",
        skills: []
    });

    const {
        vacancies,
        isLoadingVacancies: isLoading,
        companies,
        masterSkills,
        industries,
        deleteMutation,
        createSkillMutation,
        createMutation,
        updateMutation
    } = useAdminVacancies(() => {
        setIsFormOpen(false);
    });

    // Handlers
    const handleDelete = (v) => {
        setSelectedVacancy(v);
        setIsConfirmOpen(true);
    };

    const confirmDelete = () => {
        if (selectedVacancy) deleteMutation.mutate(selectedVacancy.id);
    };

    const handleEdit = async (v) => {
        setSelectedVacancy(v);
        setFormData({
            title: v.title,
            company_id: v.company_id || v.company?.id || "",
            location: v.location || "",
            type: v.type,
            payment_type: v.payment_type || "UNPAID",
            description: v.description,
            source_url: v.source_url || "",
            open_date: v.open_date ? v.open_date.split('T')[0] : new Date().toISOString().split('T')[0],
            close_date: v.close_date ? v.close_date.split('T')[0] : "",
            compensation_min: v.compensation_min || "",
            compensation_max: v.compensation_max || "",
            compensation_note: v.compensation_note || "",
            skills: []
        });
        setIsFormOpen(true);

        try {
            const detail = await vacancyService.getVacancy(v.id);
            if (detail && detail.skills) {
                const formattedSkills = detail.skills.map(s => ({
                    skill_id: s.skill_id,
                    is_mandatory: s.is_mandatory
                }));
                setFormData(prev => ({ ...prev, skills: formattedSkills }));
            } else {
                setFormData(prev => ({ ...prev, skills: [] }));
            }
        } catch (err) {
            console.error("Failed to fetch vacancy details:", err);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const cleanedSkills = (formData.skills || []).filter(s => s.skill_id !== "");
        
        let formattedSourceUrl = null;
        if (formData.source_url && formData.source_url.trim() !== "") {
            let url = formData.source_url.trim();
            if (!/^https?:\/\//i.test(url)) {
                url = "https://" + url;
            }
            formattedSourceUrl = url;
        }

        const payload = {
            title: formData.title.trim(),
            company_id: formData.company_id || null,
            description: formData.description.trim(),
            type: formData.type,
            open_date: formData.open_date ? new Date(formData.open_date).toISOString() : new Date().toISOString(),
            close_date: formData.close_date ? new Date(formData.close_date).toISOString() : null,
            location: formData.location && formData.location.trim() !== "" ? formData.location.trim() : null,
            payment_type: formData.payment_type,
            compensation_min: formData.compensation_min === "" ? null : formData.compensation_min,
            compensation_max: formData.compensation_max === "" ? null : formData.compensation_max,
            compensation_note: formData.compensation_note && formData.compensation_note.trim() !== "" ? formData.compensation_note.trim() : null,
            source_url: formattedSourceUrl,
            skills: cleanedSkills,
        };

        if (selectedVacancy && isFormOpen) {
            updateMutation.mutate({ id: selectedVacancy.id, data: payload });
        } else {
            createMutation.mutate(payload);
        }
    };

    // Filter Logic
    const filteredVacancies = vacancies?.items?.filter(v => {
        const titleMatch = v.title.toLowerCase().includes(searchTerm.toLowerCase());
        const companyMatch = (v.company?.name || "").toLowerCase().includes(searchTerm.toLowerCase());
        const matchesSearch = titleMatch || companyMatch;
        
        // Tab Filtering
        let tabMatch = true;
        if (activeTab === "scraped") tabMatch = v.is_scraped;
        else if (activeTab === "manual") tabMatch = !v.is_scraped && v.created_by;
        else if (activeTab === "verified") tabMatch = !v.is_scraped && !v.created_by;

        // Advanced Filtering
        const matchesType = typeFilter === "all" || v.type === typeFilter;
        const matchesIndustry = industryFilter === "all" || v.company?.industry === industryFilter;
        
        const isClosed = new Date(v.close_date) < new Date();
        const matchesStatus = statusFilter === "all" || (statusFilter === "closed" ? isClosed : !isClosed);

        return matchesSearch && tabMatch && matchesType && matchesIndustry && matchesStatus;
    });

    return (
        <div className="font-jakarta space-y-8 pb-32">
            {/* Header Banner */}
            <div className="bg-sky-950 py-12 px-10 rounded-[2.5rem] text-white shadow-2xl relative overflow-hidden">
                <div className="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                    <div>
                        <div className="flex items-center gap-3 mb-4">
                            <span className="bg-sky-500/20 text-sky-300 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border border-sky-500/30">
                                Management
                            </span>
                            <span className="text-sky-400 text-xs">•</span>
                            <span className="text-sky-200 text-xs font-medium">
                                Data Terakhir: {new Date().toLocaleDateString('id-ID', { 
                                    day: 'numeric', 
                                    month: 'long', 
                                    year: 'numeric',
                                    hour: '2-digit',
                                    minute: '2-digit'
                                })} WIB
                            </span>
                        </div>
                        <h1 className="text-4xl font-extrabold mb-3 tracking-tight">Kurasi Lowongan</h1>
                        <p className="text-sky-100/70 max-w-xl text-lg leading-relaxed">
                            Kelola ekosistem karir mahasiswa IPB. Verifikasi hasil scraping atau publikasikan lowongan eksklusif CDA.
                        </p>
                    </div>
                    <div className="flex gap-3">
                        <button 
                            onClick={() => {
                                setSelectedVacancy(null);
                                setFormData({
                                    title: "", company_id: "", location: "", type: "INTERNSHIP_GENERAL",
                                    payment_type: "UNPAID", description: "", source_url: "", close_date: "",
                                    open_date: new Date().toISOString().split('T')[0],
                                    compensation_min: "", compensation_max: "", compensation_note: "",
                                    skills: []
                                });
                                setIsFormOpen(true);
                            }}
                            className="bg-white text-sky-950 px-8 py-4 rounded-[1.5rem] font-extrabold flex items-center gap-2 hover:bg-sky-50 transition-all shadow-xl shadow-sky-900/40 active:scale-95"
                        >
                            <PiPlusBold size={20} />
                            Tambah Manual
                        </button>
                    </div>
                </div>
                {/* Decoration */}
                <div className="absolute top-0 right-0 w-96 h-96 bg-sky-400/10 rounded-full -mr-32 -mt-32 blur-[100px]"></div>
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-indigo-500/10 rounded-full -ml-20 -mb-20 blur-[80px]"></div>
            </div>

            {/* Toolbar & Search */}
            <div className="space-y-6">
                <div className="flex flex-col lg:flex-row gap-6 items-center justify-between">
                    <div className="flex bg-slate-100/80 p-1.5 rounded-2xl w-full lg:w-fit backdrop-blur-sm border border-slate-200/50 shadow-inner overflow-x-auto">
                        {[
                            { id: "all", label: "Semua", count: vacancies?.total || 0 },
                            { id: "verified", label: "Terverifikasi" },
                            { id: "scraped", label: "Hasil Scraping" },
                            { id: "manual", label: "Input Manual" }
                        ].map((tab) => (
                            <button 
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`whitespace-nowrap px-6 py-3 rounded-xl text-sm font-bold transition-all relative ${activeTab === tab.id ? 'bg-sky-950 text-white shadow-md shadow-sky-900/10' : 'text-slate-500 hover:text-sky-950 hover:bg-slate-50'}`}
                            >
                                {tab.label}
                            </button>
                        ))}
                    </div>

                    <div className="relative w-full lg:w-96 group">
                        <PiMagnifyingGlassBold className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-sky-600 transition-colors" />
                        <input 
                            type="text"
                            placeholder="Cari posisi atau perusahaan..."
                            className="w-full pl-12 pr-4 py-4 bg-white border border-slate-100 rounded-2xl shadow-sm text-sm focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                {/* Secondary Filters */}
                <div className="flex flex-wrap gap-4 items-center bg-white p-5 rounded-2xl shadow-sm border border-slate-100">
                    <div className="flex items-center gap-2 px-4 py-2 bg-slate-50 rounded-xl border border-slate-100">
                        <PiFunnelBold className="text-sky-600" />
                        <span className="text-xs font-extrabold text-slate-400 uppercase tracking-widest">Filter Lanjutan:</span>
                    </div>

                    {/* Status Filter */}
                    <div className="relative min-w-[160px]">
                        <select 
                            className="w-full pl-4 pr-10 py-3 bg-white border border-slate-200 rounded-xl text-xs font-bold focus:ring-2 focus:ring-sky-500/20 outline-none appearance-none cursor-pointer"
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                        >
                            <option value="all">Semua Status</option>
                            <option value="active">Aktif (Open)</option>
                            <option value="closed">Selesai (Closed)</option>
                        </select>
                        <PiCaretDown className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                    </div>

                    {/* Type Filter */}
                    <div className="relative min-w-[180px]">
                        <select 
                            className="w-full pl-4 pr-10 py-3 bg-white border border-slate-200 rounded-xl text-xs font-bold focus:ring-2 focus:ring-sky-500/20 outline-none appearance-none cursor-pointer"
                            value={typeFilter}
                            onChange={(e) => setTypeFilter(e.target.value)}
                        >
                            <option value="all">Semua Tipe</option>
                            <option value="INTERNSHIP_GENERAL">Magang Umum</option>
                            <option value="MBKM_INTERNSHIP">Magang MBKM</option>
                            <option value="MBKM_STUDY_INDEPENDENT">MBKM Studi Ind.</option>
                            <option value="FULL_TIME">Full Time</option>
                        </select>
                        <PiCaretDown className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                    </div>

                    {/* Industry Filter */}
                    <div className="relative min-w-[200px]">
                        <select 
                            className="w-full pl-4 pr-10 py-3 bg-white border border-slate-200 rounded-xl text-xs font-bold focus:ring-2 focus:ring-sky-500/20 outline-none appearance-none cursor-pointer"
                            value={industryFilter}
                            onChange={(e) => setIndustryFilter(e.target.value)}
                        >
                            <option value="all">Semua Industri</option>
                            {industries?.map(ind => (
                                <option key={ind} value={ind}>{ind}</option>
                            ))}
                        </select>
                        <PiCaretDown className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                    </div>

                    <button 
                        onClick={() => {
                            setSearchTerm("");
                            setTypeFilter("all");
                            setStatusFilter("all");
                            setIndustryFilter("all");
                            setActiveTab("all");
                        }}
                        className="ml-auto text-[10px] font-extrabold text-slate-400 hover:text-red-500 uppercase tracking-widest transition-colors"
                    >
                        Reset Filter
                    </button>
                </div>
            </div>

            {/* Content List */}
            <div className="grid grid-cols-1 gap-5">
                {isLoading ? (
                    <div className="p-32 text-center text-slate-400 bg-white rounded-[2rem] border border-dashed border-slate-200">
                        <div className="flex flex-col items-center gap-4">
                            <div className="w-12 h-12 border-4 border-sky-100 border-t-sky-600 rounded-full animate-spin"></div>
                            <p className="font-bold tracking-widest uppercase text-xs">Memuat Basis Data...</p>
                        </div>
                    </div>
                ) : filteredVacancies?.length > 0 ? (
                    filteredVacancies.map((vacancy) => {
                        const isClosed = new Date(vacancy.close_date) < new Date();
                        return (
                            <div key={vacancy.id} className={`bg-white p-6 rounded-[2.5rem] shadow-sm border ${isClosed ? 'border-red-100 opacity-80' : 'border-slate-100'} flex flex-col md:flex-row justify-between items-center gap-6 hover:shadow-xl hover:border-sky-100 transition-all group relative overflow-hidden`}>
                                {/* Source Indicator Line */}
                                <div className={`absolute top-0 bottom-0 left-0 w-1.5 ${vacancy.is_scraped ? 'bg-sky-500' : 'bg-emerald-500'}`}></div>
                                
                                <div className="flex gap-6 items-center w-full">
                                    <div className="w-20 h-20 rounded-[1.5rem] bg-slate-50 flex items-center justify-center p-4 border border-slate-100 shrink-0 group-hover:scale-105 transition-transform duration-300">
                                        <img 
                                            src={vacancy.company?.logo_url || "/logo/placeholder-company.png"} 
                                            alt="Logo"
                                            className="w-full h-full object-contain mix-blend-multiply"
                                            onError={(e) => e.target.src = "/logo/placeholder-company.png"}
                                        />
                                    </div>
                                    <div className="flex-1 space-y-3">
                                        <div className="flex flex-wrap items-center gap-2">
                                            <h3 className="font-extrabold text-slate-900 text-xl tracking-tight leading-tight">{vacancy.title}</h3>
                                            <div className="flex gap-1.5">
                                                {isClosed ? (
                                                    <span className="flex items-center gap-1 bg-red-50 text-red-600 px-2 py-0.5 rounded-lg text-[9px] font-black uppercase border border-red-100">
                                                        <PiXCircleFill /> Closed
                                                    </span>
                                                ) : (
                                                    <span className="flex items-center gap-1 bg-emerald-50 text-emerald-600 px-2 py-0.5 rounded-lg text-[9px] font-black uppercase border border-emerald-100">
                                                        <PiCheckCircleFill /> Active
                                                    </span>
                                                )}
                                                {vacancy.is_scraped && (
                                                    <span className="bg-sky-50 text-sky-600 px-2 py-0.5 rounded-lg text-[9px] font-black uppercase border border-sky-100">Scraped</span>
                                                )}
                                            </div>
                                        </div>
                                        <div className="flex flex-wrap gap-x-6 gap-y-2 text-slate-500 text-sm font-semibold">
                                            <div className="flex items-center gap-1.5">
                                                <PiBuildingsBold className="text-sky-700" size={18} />
                                                <span>{vacancy.company?.name}</span>
                                            </div>
                                            <div className="flex items-center gap-1.5 text-slate-400">
                                                <PiMapPinBold size={18} />
                                                <span>{vacancy.location || "Jakarta, Remote"}</span>
                                            </div>
                                            <div className="flex items-center gap-1.5 text-slate-400">
                                                <PiCalendarBold size={18} />
                                                <span className={isClosed ? "text-red-500 font-bold" : ""}>
                                                    Deadline: {new Date(vacancy.close_date).toLocaleDateString('id-ID', { day: 'numeric', month: 'short' })}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="flex gap-2 shrink-0">
                                    <button 
                                        onClick={() => handleEdit(vacancy)}
                                        className="p-4 text-slate-400 hover:text-sky-600 hover:bg-sky-50 rounded-2xl transition-all shadow-sm border border-transparent hover:border-sky-100" 
                                        title="Edit Detail"
                                    >
                                        <PiPencilSimpleBold size={24} />
                                    </button>
                                    <button 
                                        onClick={() => {
                                            // Duplicate logic
                                            const duplicateData = { ...vacancy, title: `${vacancy.title} (Copy)`, id: undefined };
                                            setFormData({
                                                title: duplicateData.title,
                                                company_id: vacancy.company_id,
                                                location: vacancy.location || "",
                                                type: vacancy.type,
                                                payment_type: vacancy.payment_type || "UNPAID",
                                                description: vacancy.description,
                                                source_url: vacancy.source_url || "",
                                                open_date: new Date().toISOString().split('T')[0],
                                                close_date: vacancy.close_date ? vacancy.close_date.split('T')[0] : "",
                                                compensation_min: vacancy.compensation_min || "",
                                                compensation_max: vacancy.compensation_max || "",
                                                compensation_note: vacancy.compensation_note || "",
                                                skills: []
                                            });
                                            setIsFormOpen(true);
                                            setSelectedVacancy(null); // Set to null so it creates new

                                            // Fetch detailed skills for duplicated vacancy
                                            vacancyService.getVacancy(vacancy.id).then(detail => {
                                                if (detail && detail.skills) {
                                                    const formattedSkills = detail.skills.map(s => ({
                                                        skill_id: s.skill_id,
                                                        is_mandatory: s.is_mandatory
                                                    }));
                                                    setFormData(prev => ({ ...prev, skills: formattedSkills }));
                                                } else {
                                                    setFormData(prev => ({ ...prev, skills: [] }));
                                                }
                                            }).catch(err => {
                                                console.error("Failed to fetch duplicate skills:", err);
                                                setFormData(prev => ({ ...prev, skills: [] }));
                                            });
                                        }}
                                        className="p-4 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-2xl transition-all shadow-sm border border-transparent hover:border-amber-100" 
                                        title="Duplikat"
                                    >
                                        <PiPlusBold size={24} />
                                    </button>
                                    <button 
                                        onClick={() => handleDelete(vacancy)}
                                        className="p-4 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-2xl transition-all shadow-sm border border-transparent hover:border-red-100" 
                                        title="Hapus"
                                    >
                                        <PiTrashBold size={24} />
                                    </button>
                                </div>
                            </div>
                        );
                    })
                ) : (
                    <div className="p-32 text-center text-slate-400 bg-white rounded-[2rem] border border-dashed border-slate-200 italic">
                        Tidak ada lowongan dalam kategori ini.
                    </div>
                )}
            </div>

            {/* Add/Edit Modal */}
            {isFormOpen && (
                <div className="fixed inset-0 z-[80] flex items-center justify-center p-4">
                    <div className="absolute inset-0 bg-sky-950/60 backdrop-blur-md" onClick={() => setIsFormOpen(false)}></div>
                    <div className="relative bg-white rounded-[2.5rem] shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col animate-in slide-in-from-bottom-10 duration-300">
                        {/* Modal Header */}
                        <div className="p-10 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                            <div>
                                <h2 className="text-2xl font-extrabold text-slate-900">{selectedVacancy ? "Perbarui Lowongan" : "Tambah Lowongan Baru"}</h2>
                                <p className="text-slate-500 text-sm mt-1">Lengkapi data untuk publikasi ke portal mahasiswa.</p>
                            </div>
                            <button onClick={() => setIsFormOpen(false)} className="p-3 hover:bg-white rounded-2xl transition-all border border-transparent hover:border-slate-200">
                                <PiXCircleFill size={32} className="text-slate-400" />
                            </button>
                        </div>

                        {/* Modal Body */}
                        <form id="vacancy-form" onSubmit={handleSubmit} className="p-10 pb-44 overflow-y-auto flex-1 space-y-8 text-sm">
                            <div className="grid grid-cols-2 gap-6">
                                <div className="col-span-2 space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Judul Posisi</label>
                                    <input 
                                        required
                                        className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                        placeholder="Contoh: Backend Engineer Intern"
                                        value={formData.title}
                                        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Perusahaan</label>
                                    <div className="relative">
                                        <select 
                                            required
                                            className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium appearance-none cursor-pointer"
                                            value={formData.company_id}
                                            onChange={(e) => setFormData({ ...formData, company_id: e.target.value })}
                                        >
                                            <option value="">Pilih Perusahaan</option>
                                            {companies?.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                                        </select>
                                        <PiCaretDown size={18} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Tipe Lowongan</label>
                                    <div className="relative">
                                        <select 
                                            className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium appearance-none cursor-pointer"
                                            value={formData.type}
                                            onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                                        >
                                            <option value="INTERNSHIP_GENERAL">Umum</option>
                                            <option value="MBKM_INTERNSHIP">MBKM Magang</option>
                                            <option value="MBKM_STUDY_INDEPENDENT">Studi Independen</option>
                                            <option value="FULL_TIME">Lulusan Baru (Full-time)</option>
                                        </select>
                                        <PiCaretDown size={18} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Lokasi</label>
                                    <input 
                                        className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                        placeholder="Contoh: Jakarta, Remote"
                                        value={formData.location}
                                        onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Buka Lowongan</label>
                                    <input 
                                        type="date"
                                        required
                                        className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                        value={formData.open_date}
                                        onChange={(e) => setFormData({ ...formData, open_date: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Tutup/Deadline</label>
                                    <input 
                                        type="date"
                                        required
                                        className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                        value={formData.close_date}
                                        onChange={(e) => setFormData({ ...formData, close_date: e.target.value })}
                                    />
                                </div>

                                <div className="space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Tipe Pembayaran</label>
                                    <div className="relative">
                                        <select 
                                            className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium appearance-none cursor-pointer"
                                            value={formData.payment_type}
                                            onChange={(e) => setFormData({ ...formData, payment_type: e.target.value })}
                                        >
                                            <option value="UNPAID">Unpaid (Sukarela)</option>
                                            <option value="PAID">Paid (Berbayar)</option>
                                            <option value="ALLOWANCE_ONLY">Uang Saku Saja</option>
                                        </select>
                                        <PiCaretDown size={18} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Catatan Kompensasi</label>
                                    <input 
                                        className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                        placeholder="Contoh: Sesuai UMR, Negotiable"
                                        value={formData.compensation_note}
                                        onChange={(e) => setFormData({ ...formData, compensation_note: e.target.value })}
                                    />
                                </div>

                                {formData.payment_type !== "UNPAID" && (
                                    <>
                                        <div className="space-y-2">
                                            <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Kompensasi Min (Rp)</label>
                                            <input 
                                                type="number"
                                                className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                                placeholder="0"
                                                value={formData.compensation_min}
                                                onChange={(e) => setFormData({ ...formData, compensation_min: e.target.value })}
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Kompensasi Max (Rp)</label>
                                            <input 
                                                type="number"
                                                className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                                placeholder="0"
                                                value={formData.compensation_max}
                                                onChange={(e) => setFormData({ ...formData, compensation_max: e.target.value })}
                                            />
                                        </div>
                                    </>
                                )}

                                <div className="col-span-2 space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Deskripsi Pekerjaan</label>
                                    <textarea 
                                        required
                                        rows={5}
                                        className="w-full p-6 bg-slate-50 border border-slate-200 rounded-[2rem] focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium leading-relaxed"
                                        placeholder="Jelaskan detail pekerjaan, kualifikasi, dan benefit..."
                                        value={formData.description}
                                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    />
                                </div>
                                <div className="col-span-2 space-y-2">
                                    <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">URL Sumber (Opsional)</label>
                                    <input 
                                        className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                        placeholder="https://company.com/career/page"
                                        value={formData.source_url}
                                        onChange={(e) => setFormData({ ...formData, source_url: e.target.value })}
                                    />
                                </div>

                                {/* Kualifikasi & Skill Section */}
                                <div className="col-span-2 space-y-4 border-t border-slate-100 pt-6">
                                    <div className="flex justify-between items-center">
                                        <label className="font-bold text-slate-700 uppercase tracking-wider text-[11px]">Kualifikasi & Keahlian (Skills)</label>
                                    </div>

                                    {formData.skills && formData.skills.length > 0 ? (
                                        <div className="space-y-3">
                                            {formData.skills.map((skillItem, index) => {
                                                const selectedSkill = masterSkills?.find(s => s.id === skillItem.skill_id);
                                                const selectedSkillIds = formData.skills?.map(sk => sk.skill_id).filter(id => !!id) || [];
                                                const filteredSkills = masterSkills?.filter(s =>
                                                    s.name.toLowerCase().includes(skillSearchQuery.toLowerCase()) &&
                                                    !selectedSkillIds.includes(s.id)
                                                ) || [];
                                                const isPerfectMatch = filteredSkills.some(s => s.name.toLowerCase() === skillSearchQuery.trim().toLowerCase());

                                                return (
                                                    <div 
                                                        key={index} 
                                                        className="flex gap-4 items-center bg-slate-50 p-4 rounded-2xl border border-slate-100 relative"
                                                        style={{ zIndex: openSkillDropdownIndex === index ? 40 : 10 }}
                                                    >
                                                        {/* Backdrop overlay to close dropdown if open */}
                                                        {openSkillDropdownIndex === index && (
                                                            <div className="fixed inset-0 z-20 cursor-default" onClick={() => setOpenSkillDropdownIndex(null)} />
                                                        )}

                                                        <div className="flex-1 relative z-30">
                                                            <input
                                                                type="text"
                                                                required={!skillItem.skill_id}
                                                                autoComplete="new-skill-search"
                                                                className="w-full p-3 bg-white border border-slate-200 rounded-xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium text-xs pr-10 cursor-text"
                                                                placeholder="Cari atau ketik keahlian baru..."
                                                                value={openSkillDropdownIndex === index ? skillSearchQuery : (selectedSkill ? `${selectedSkill.name} (${selectedSkill.category || 'General'})` : "")}
                                                                onFocus={() => {
                                                                    setOpenSkillDropdownIndex(index);
                                                                    setSkillSearchQuery("");
                                                                }}
                                                                onChange={(e) => setSkillSearchQuery(e.target.value)}
                                                                onKeyDown={async (e) => {
                                                                    if (e.key === "Enter") {
                                                                        e.preventDefault();
                                                                        const newName = skillSearchQuery.trim();
                                                                        if (!newName) return;

                                                                        // Check perfect match
                                                                        const perfectMatch = masterSkills?.find(s => s.name.toLowerCase() === newName.toLowerCase());
                                                                        if (perfectMatch) {
                                                                            const newSkills = [...formData.skills];
                                                                            newSkills[index].skill_id = perfectMatch.id;
                                                                            setFormData({ ...formData, skills: newSkills });
                                                                            setOpenSkillDropdownIndex(null);
                                                                            setSkillSearchQuery("");
                                                                        } else {
                                                                            try {
                                                                                const newSkill = await createSkillMutation.mutateAsync({
                                                                                    name: newName,
                                                                                    category: "Technical"
                                                                                });
                                                                                const newSkills = [...formData.skills];
                                                                                newSkills[index].skill_id = newSkill.id;
                                                                                setFormData({ ...formData, skills: newSkills });
                                                                                setOpenSkillDropdownIndex(null);
                                                                                setSkillSearchQuery("");
                                                                            } catch (err) {
                                                                                console.error(err);
                                                                            }
                                                                        }
                                                                    }
                                                                }}
                                                            />
                                                            <PiCaretDown size={14} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />

                                                            {/* Dropdown Menu */}
                                                            {openSkillDropdownIndex === index && (
                                                                <div className="absolute top-full left-0 right-0 mt-1 max-h-60 overflow-y-auto bg-white border border-slate-200 rounded-xl shadow-xl p-2 space-y-1 z-30">
                                                                    {filteredSkills.slice(0, 15).map(s => (
                                                                        <button
                                                                            key={s.id}
                                                                            type="button"
                                                                            onClick={() => {
                                                                                const newSkills = [...formData.skills];
                                                                                newSkills[index].skill_id = s.id;
                                                                                setFormData({ ...formData, skills: newSkills });
                                                                                setOpenSkillDropdownIndex(null);
                                                                            }}
                                                                            className="w-full text-left px-3 py-2 text-xs text-slate-700 hover:bg-sky-50 hover:text-sky-800 rounded-lg transition-colors font-medium flex justify-between items-center"
                                                                        >
                                                                            <span>{s.name}</span>
                                                                            <span className="text-[10px] bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded uppercase font-bold">{s.category || "General"}</span>
                                                                        </button>
                                                                    ))}

                                                                    {skillSearchQuery.trim() !== "" && !isPerfectMatch && (
                                                                        <div className="p-2 border border-slate-100 rounded-xl bg-slate-50 space-y-2 mt-1 relative z-30">
                                                                            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider px-1">Tambah Keahlian Baru &quot;{skillSearchQuery}&quot; sebagai:</p>
                                                                            <div className="flex gap-2">
                                                                                {["Technical", "Soft Skill", "General"].map(cat => (
                                                                                    <button
                                                                                        key={cat}
                                                                                        type="button"
                                                                                        disabled={createSkillMutation.isPending}
                                                                                        onClick={async () => {
                                                                                            const newName = skillSearchQuery.trim();
                                                                                            try {
                                                                                                const newSkill = await createSkillMutation.mutateAsync({
                                                                                                    name: newName,
                                                                                                    category: cat
                                                                                                });
                                                                                                const newSkills = [...formData.skills];
                                                                                                newSkills[index].skill_id = newSkill.id;
                                                                                                setFormData({ ...formData, skills: newSkills });
                                                                                                setOpenSkillDropdownIndex(null);
                                                                                                setSkillSearchQuery("");
                                                                                            } catch (err) {
                                                                                                console.error(err);
                                                                                            }
                                                                                        }}
                                                                                        className="flex-1 py-2 px-1 hover:bg-sky-50 text-slate-700 hover:text-sky-800 text-[10px] font-bold rounded-lg border border-slate-200 hover:border-sky-300 transition-all flex items-center justify-center gap-1 active:scale-95 disabled:opacity-50 bg-white"
                                                                                    >
                                                                                        {createSkillMutation.isPending ? (
                                                                                            <PiSpinnerGap className="animate-spin text-slate-400" size={10} />
                                                                                        ) : null}
                                                                                        <span>{cat}</span>
                                                                                    </button>
                                                                                ))}
                                                                            </div>
                                                                        </div>
                                                                    )}

                                                                    {filteredSkills.length === 0 && skillSearchQuery.trim() === "" && (
                                                                        <p className="text-center text-xs text-slate-400 py-3 italic">Ketik untuk mencari...</p>
                                                                    )}
                                                                </div>
                                                            )}
                                                        </div>

                                                        <div className="flex items-center gap-2 relative z-30">
                                                            <input
                                                                type="checkbox"
                                                                id={`mandatory-${index}`}
                                                                checked={skillItem.is_mandatory}
                                                                onChange={(e) => {
                                                                    const newSkills = [...formData.skills];
                                                                    newSkills[index].is_mandatory = e.target.checked;
                                                                    setFormData({ ...formData, skills: newSkills });
                                                                }}
                                                                className="w-4 h-4 text-sky-600 border-slate-300 rounded focus:ring-sky-500"
                                                            />
                                                            <label htmlFor={`mandatory-${index}`} className="text-xs text-slate-600 font-bold select-none cursor-pointer">Wajib</label>
                                                        </div>

                                                        <button
                                                            type="button"
                                                            onClick={() => {
                                                                const newSkills = formData.skills.filter((_, i) => i !== index);
                                                                setFormData({ ...formData, skills: newSkills });
                                                            }}
                                                            className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all relative z-30"
                                                            title="Hapus"
                                                        >
                                                            <PiTrashBold size={16} />
                                                        </button>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    ) : (
                                        <div className="text-center py-6 border border-dashed border-slate-200 rounded-2xl bg-slate-50 text-xs text-slate-400 italic">
                                            Belum ada kualifikasi skill yang ditentukan untuk lowongan ini.
                                        </div>
                                    )}

                                    {/* Dashed placeholder add button below the list */}
                                    <button
                                        type="button"
                                        onClick={() => {
                                            setFormData(prev => ({
                                                ...prev,
                                                skills: [...(prev.skills || []), { skill_id: "", is_mandatory: true }]
                                            }));
                                        }}
                                        className="w-full py-4 px-6 border border-dashed border-slate-200 hover:border-sky-500 hover:bg-sky-50/10 rounded-2xl text-xs text-slate-500 hover:text-sky-600 bg-white transition-all font-bold flex items-center justify-center gap-2 cursor-pointer relative z-30"
                                    >
                                        <PiPlusBold size={14} />
                                        <span>Tambah Kebutuhan Keahlian (Skills)</span>
                                    </button>
                                </div>
                            </div>
                        </form>

                        {/* Modal Footer */}
                        <div className="p-8 bg-slate-50/80 border-t border-slate-100 flex gap-4">
                            <button 
                                type="button"
                                onClick={() => setIsFormOpen(false)}
                                className="flex-1 py-4 px-6 rounded-2xl font-bold text-slate-500 hover:bg-white transition-all border border-transparent hover:border-slate-200"
                            >
                                Batal
                            </button>
                            <button 
                                form="vacancy-form"
                                type="submit"
                                disabled={createMutation.isPending || updateMutation.isPending}
                                className="flex-[2] py-4 px-6 rounded-2xl font-extrabold text-white bg-sky-950 hover:bg-sky-900 shadow-xl shadow-sky-900/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                            >
                                {createMutation.isPending || updateMutation.isPending ? (
                                    <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                                ) : (
                                    selectedVacancy ? "Simpan Perubahan" : "Publikasikan Lowongan"
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Deletion Confirm */}
            <ConfirmModal 
                isOpen={isConfirmOpen}
                onClose={() => setIsConfirmOpen(false)}
                onConfirm={confirmDelete}
                title="Hapus Lowongan?"
                message={`Anda akan menghapus "${selectedVacancy?.title}". Tindakan ini tidak dapat dibatalkan dan akan menghapus semua data lamaran terkait.`}
            />
        </div>
    );
}

export default AdminVacancies;
