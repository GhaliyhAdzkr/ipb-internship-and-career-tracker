import { useState } from "react";
import { 
    PiPlusBold, 
    PiMagnifyingGlassBold, 
    PiPencilSimpleBold, 
    PiTrashBold,
    PiGlobeBold,
    PiIdentificationCardBold,
    PiMapPinBold,
    PiXCircleFill
} from "react-icons/pi";
import { useAdminCompanies } from "../../hooks/useAdminCompanies";
import adminService from "../../services/adminService";
import ConfirmModal from "../../components/ConfirmModal";
import toast from "react-hot-toast";

function AdminCompanies() {
    const [searchTerm, setSearchTerm] = useState("");
    const [isConfirmOpen, setIsConfirmOpen] = useState(false);
    const [selectedCompany, setSelectedCompany] = useState(null);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [formData, setFormData] = useState({
        name: "",
        industry: "",
        website_url: "",
        address: "",
        logo_url: ""
    });

    const {
        companies,
        isLoadingCompanies: isLoading,
        deleteMutation,
        createMutation,
        updateMutation
    } = useAdminCompanies(() => {
        setIsFormOpen(false);
    });

    const handleDelete = (company) => {
        setSelectedCompany(company);
        setIsConfirmOpen(true);
    };

    const confirmDelete = () => {
        if (selectedCompany) deleteMutation.mutate(selectedCompany.id);
    };

    const handleEdit = (company) => {
        setSelectedCompany(company);
        setFormData({
            name: company.name,
            industry: company.industry || "",
            website_url: company.website_url || "",
            address: company.address || "",
            logo_url: company.logo_url || ""
        });
        setIsFormOpen(true);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (selectedCompany) {
            updateMutation.mutate({ id: selectedCompany.id, data: formData });
        } else {
            createMutation.mutate(formData);
        }
    };

    const filteredCompanies = companies?.filter(c => 
        c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.industry?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="font-jakarta space-y-8 pb-20">
            {/* Header Banner */}
            <div className="bg-sky-950 py-12 px-10 rounded-[2.5rem] text-white shadow-xl relative overflow-hidden">
                <div className="relative z-10 flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-extrabold mb-2 tracking-tight">Kemitraan Strategis</h1>
                        <p className="text-sky-200 max-w-xl text-lg opacity-80 font-medium">
                            Kelola data perusahaan mitra CDA IPB untuk mendukung ekosistem karir mahasiswa.
                        </p>
                    </div>
                    <button 
                        onClick={() => {
                            setSelectedCompany(null);
                            setFormData({ name: "", industry: "", website_url: "", address: "", logo_url: "" });
                            setIsFormOpen(true);
                        }}
                        className="bg-white text-sky-950 px-8 py-4 rounded-2xl font-extrabold flex items-center gap-2 hover:bg-sky-50 transition-all shadow-xl shadow-sky-900/30 active:scale-95"
                    >
                        <PiPlusBold size={20} />
                        Tambah Mitra
                    </button>
                </div>
                <div className="absolute top-0 right-0 w-80 h-80 bg-white/5 rounded-full -mr-24 -mt-24 blur-3xl"></div>
            </div>

            {/* Toolbar */}
            <div className="flex flex-col md:flex-row gap-4 items-center justify-between bg-white p-5 rounded-[2rem] shadow-sm border border-slate-100">
                <div className="relative w-full md:w-96 group">
                    <PiMagnifyingGlassBold className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-sky-600 transition-colors" />
                    <input 
                        type="text"
                        placeholder="Cari nama perusahaan atau industri..."
                        className="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-100 rounded-2xl text-sm focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            {/* Companies Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {isLoading ? (
                    <div className="lg:col-span-2 p-32 text-center text-slate-400 bg-white rounded-2xl border border-dashed border-slate-200">
                        Memuat data mitra...
                    </div>
                ) : filteredCompanies?.length > 0 ? (
                    filteredCompanies.map((company) => (
                        <div key={company.id} className="bg-white p-7 rounded-2xl shadow-sm border border-slate-100 flex items-start gap-8 hover:shadow-xl hover:border-sky-100 transition-all group">
                            <div className="w-24 h-24 rounded-3xl bg-slate-50 flex items-center justify-center p-5 border border-slate-50 shrink-0 group-hover:scale-110 transition-transform duration-500 shadow-inner">
                                <img 
                                    src={company.logo_url || "/logo/placeholder-company.png"} 
                                    alt={company.name}
                                    className="w-full h-full object-contain mix-blend-multiply"
                                    onError={(e) => e.target.src = "/logo/placeholder-company.png"}
                                />
                            </div>
                            <div className="flex-1 space-y-4">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="font-extrabold text-slate-900 text-xl leading-tight tracking-tight">{company.name}</h3>
                                        <p className="text-sky-600 text-[10px] font-extrabold uppercase tracking-[0.2em] mt-1.5">{company.industry || "Industri Belum Diatur"}</p>
                                    </div>
                                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
                                        <button 
                                            onClick={() => handleEdit(company)}
                                            className="p-3 text-slate-400 hover:text-sky-600 hover:bg-sky-50 rounded-xl transition-all shadow-sm border border-transparent hover:border-sky-100" title="Edit"
                                        >
                                            <PiPencilSimpleBold size={20} />
                                        </button>
                                        <button 
                                            onClick={() => handleDelete(company)}
                                            className="p-3 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all shadow-sm border border-transparent hover:border-red-100" 
                                            title="Hapus"
                                        >
                                            <PiTrashBold size={20} />
                                        </button>
                                    </div>
                                </div>
                                
                                <div className="space-y-2 pt-3 border-t border-slate-50">
                                    <div className="flex items-center gap-3 text-slate-500 text-xs font-medium">
                                        <div className="p-1.5 bg-slate-50 rounded-lg"><PiGlobeBold className="text-slate-400" /></div>
                                        <span className="truncate">{company.website_url || "Website tidak tersedia"}</span>
                                    </div>
                                    <div className="flex items-center gap-3 text-slate-500 text-xs font-medium">
                                        <div className="p-1.5 bg-slate-50 rounded-lg"><PiMapPinBold className="text-slate-400" /></div>
                                        <span className="line-clamp-1">{company.address || "Alamat belum diatur"}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="lg:col-span-2 p-32 text-center text-slate-400 bg-white rounded-[2.5rem] border border-dashed border-slate-200 italic font-medium">
                        Tidak ada mitra yang ditemukan.
                    </div>
                )}
            </div>

            {/* Add/Edit Modal */}
            {isFormOpen && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
                    <div className="absolute inset-0 bg-sky-950/60 backdrop-blur-md" onClick={() => setIsFormOpen(false)}></div>
                    <div className="relative bg-white rounded-[2.5rem] shadow-2xl w-full max-w-xl animate-in slide-in-from-bottom-10 duration-300 overflow-hidden">
                        <div className="p-10 border-b border-slate-100 flex justify-between items-center">
                            <h2 className="text-2xl font-extrabold text-slate-900">{selectedCompany ? "Perbarui Mitra" : "Tambah Mitra Baru"}</h2>
                            <button onClick={() => setIsFormOpen(false)} className="p-2 hover:bg-slate-50 rounded-2xl transition-all">
                                <PiXCircleFill size={32} className="text-slate-400" />
                            </button>
                        </div>
                        
                        <form onSubmit={handleSubmit} className="p-10 space-y-6">
                            <div className="space-y-2">
                                <label className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest">Nama Perusahaan</label>
                                <input 
                                    required
                                    className="w-full p-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-bold"
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest">Industri</label>
                                <input 
                                    className="w-full p-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                    value={formData.industry}
                                    onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest">Website URL</label>
                                <input 
                                    className="w-full p-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                    value={formData.website_url}
                                    onChange={(e) => setFormData({ ...formData, website_url: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest">Alamat Perusahaan</label>
                                <textarea 
                                    className="w-full p-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                    rows={3}
                                    value={formData.address}
                                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest block">Logo Perusahaan</label>
                                <div className="flex items-center gap-6">
                                    <div className="w-24 h-24 rounded-3xl bg-slate-50 border border-dashed border-slate-200 flex items-center justify-center p-3 shrink-0 overflow-hidden relative shadow-inner">
                                        {formData.logo_url ? (
                                            <img 
                                                src={formData.logo_url} 
                                                alt="Preview logo" 
                                                className="w-full h-full object-contain"
                                            />
                                        ) : (
                                            <div className="text-center space-y-1">
                                                <div className="text-slate-400 text-xs font-semibold">No Logo</div>
                                            </div>
                                        )}
                                        {isUploading && (
                                            <div className="absolute inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center">
                                                <div className="w-6 h-6 border-2 border-sky-600 border-t-transparent rounded-full animate-spin"></div>
                                            </div>
                                        )}
                                    </div>
                                    <div className="flex-1 space-y-2">
                                        <div className="relative">
                                            <input 
                                                type="file"
                                                accept="image/*"
                                                id="logo-upload"
                                                className="hidden"
                                                onChange={async (e) => {
                                                    const file = e.target.files[0];
                                                    if (!file) return;
                                                    
                                                    // Validate size
                                                    if (file.size > 10 * 1024 * 1024) {
                                                        toast.error("Ukuran logo maksimal 10MB");
                                                        return;
                                                    }
                                                    
                                                    try {
                                                        setIsUploading(true);
                                                        const res = await adminService.uploadCompanyLogo(file);
                                                        setFormData(prev => ({ ...prev, logo_url: res.logo_url }));
                                                        toast.success("Logo berhasil diunggah!");
                                                    } catch (err) {
                                                        toast.error(err?.response?.data?.detail || "Gagal mengunggah logo");
                                                    } finally {
                                                        setIsUploading(false);
                                                    }
                                                }}
                                                disabled={isUploading}
                                            />
                                            <label 
                                                htmlFor="logo-upload"
                                                className={`inline-flex items-center justify-center px-5 py-3 rounded-xl border border-slate-200 bg-white text-xs font-extrabold text-slate-700 shadow-sm hover:bg-slate-50 cursor-pointer active:scale-95 transition-all gap-2 ${isUploading ? 'opacity-50 pointer-events-none' : ''}`}
                                            >
                                                {isUploading ? "Mengunggah..." : "Pilih File Logo"}
                                            </label>
                                        </div>
                                        <p className="text-[10px] text-slate-400 font-medium leading-relaxed">
                                            Format yang didukung: PNG, JPG, WEBP. Maksimal ukuran file 10MB.
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <button 
                                type="submit"
                                className="w-full py-5 bg-sky-950 text-white rounded-2xl font-extrabold shadow-xl shadow-sky-900/20 hover:bg-sky-900 transition-all active:scale-95"
                            >
                                {selectedCompany ? "Simpan Perubahan" : "Tambahkan Mitra"}
                            </button>
                        </form>
                    </div>
                </div>
            )}

            <ConfirmModal 
                isOpen={isConfirmOpen}
                onClose={() => setIsConfirmOpen(false)}
                onConfirm={confirmDelete}
                title="Hapus Kemitraan?"
                message={`Anda akan menghapus "${selectedCompany?.name}". Perusahaan ini tidak akan lagi muncul sebagai opsi dalam pembuatan lowongan.`}
            />
        </div>
    );
}

export default AdminCompanies;
