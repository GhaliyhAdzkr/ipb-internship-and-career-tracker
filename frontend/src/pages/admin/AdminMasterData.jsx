import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { 
    PiPlusBold, 
    PiMagnifyingGlassBold, 
    PiPencilSimpleBold, 
    PiTrashBold,
    PiGraduationCapBold,
    PiWrenchBold,
    PiTagBold,
    PiXCircleFill,
    PiBooksBold,
    PiIdentificationBadgeBold
} from "react-icons/pi";
import adminService from "../../services/adminService";
import ConfirmModal from "../../components/ConfirmModal";
import toast from "react-hot-toast";

function AdminMasterData() {
    const queryClient = useQueryClient();
    const [activeTab, setActiveTab] = useState("departments");
    const [searchTerm, setSearchTerm] = useState("");
    const [isConfirmOpen, setIsConfirmOpen] = useState(false);
    const [itemToDelete, setItemToDelete] = useState(null);
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const [formData, setFormData] = useState({});

    // Queries
    const { data: departments, isLoading: loadingDepts } = useQuery({
        queryKey: ["admin", "departments"],
        queryFn: adminService.getDepartments
    });

    const { data: skills, isLoading: loadingSkills } = useQuery({
        queryKey: ["admin", "skills"],
        queryFn: adminService.getSkills
    });

    // Mutations
    const deleteDeptMutation = useMutation({
        mutationFn: adminService.deleteDepartment,
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "departments"]);
            toast.success("Departemen berhasil dihapus");
        }
    });

    const deleteSkillMutation = useMutation({
        mutationFn: adminService.deleteSkill,
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "skills"]);
            toast.success("Skill berhasil dihapus");
        }
    });

    const createDeptMutation = useMutation({
        mutationFn: adminService.createDepartment,
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "departments"]);
            setIsFormOpen(false);
            toast.success("Departemen baru ditambahkan");
        }
    });

    const updateDeptMutation = useMutation({
        mutationFn: ({ id, data }) => adminService.updateDepartment(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "departments"]);
            setIsFormOpen(false);
            toast.success("Data departemen diperbarui");
        }
    });

    const createSkillMutation = useMutation({
        mutationFn: adminService.createSkill,
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "skills"]);
            setIsFormOpen(false);
            toast.success("Skill baru ditambahkan");
        }
    });

    const updateSkillMutation = useMutation({
        mutationFn: ({ id, data }) => adminService.updateSkill(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "skills"]);
            setIsFormOpen(false);
            toast.success("Data skill diperbarui");
        }
    });

    // Handlers
    const handleDeleteClick = (item) => {
        setItemToDelete(item);
        setIsConfirmOpen(true);
    };

    const confirmDelete = () => {
        if (!itemToDelete) return;
        if (activeTab === "departments") deleteDeptMutation.mutate(itemToDelete.id);
        else deleteSkillMutation.mutate(itemToDelete.id);
    };

    const handleEditClick = (item) => {
        setSelectedItem(item);
        if (activeTab === "departments") {
            setFormData({ name: item.name, code: item.code, faculty: item.faculty });
        } else {
            setFormData({ name: item.name, category: item.category || "" });
        }
        setIsFormOpen(true);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (activeTab === "departments") {
            if (selectedItem) updateDeptMutation.mutate({ id: selectedItem.id, data: formData });
            else createDeptMutation.mutate(formData);
        } else {
            if (selectedItem) updateSkillMutation.mutate({ id: selectedItem.id, data: formData });
            else createSkillMutation.mutate(formData);
        }
    };

    const filteredData = activeTab === "departments" 
        ? departments?.filter(d => d.name.toLowerCase().includes(searchTerm.toLowerCase()) || d.code.toLowerCase().includes(searchTerm.toLowerCase()))
        : skills?.filter(s => s.name.toLowerCase().includes(searchTerm.toLowerCase()) || s.category?.toLowerCase().includes(searchTerm.toLowerCase()));

    return (
        <div className="font-jakarta space-y-8 pb-32">
            {/* Header Banner */}
            <div className="bg-sky-950 py-12 px-10 rounded-[2.5rem] text-white shadow-xl relative overflow-hidden">
                <div className="relative z-10 flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-extrabold mb-2 tracking-tight">Parameter Sistem</h1>
                        <p className="text-sky-200 max-w-xl text-lg opacity-80 font-medium">
                            Kelola data dasar Program Studi dan katalog Keahlian untuk standarisasi profil mahasiswa.
                        </p>
                    </div>
                    <button 
                        onClick={() => {
                            setSelectedItem(null);
                            setFormData(activeTab === "departments" ? { name: "", code: "", faculty: "" } : { name: "", category: "" });
                            setIsFormOpen(true);
                        }}
                        className="bg-white text-sky-950 px-8 py-4 rounded-2xl font-extrabold flex items-center gap-2 hover:bg-sky-50 transition-all shadow-xl shadow-sky-900/30 active:scale-95"
                    >
                        <PiPlusBold size={20} />
                        Tambah Data
                    </button>
                </div>
                <div className="absolute top-0 right-0 w-80 h-80 bg-white/5 rounded-full -mr-24 -mt-24 blur-3xl"></div>
            </div>

            {/* Tab Navigation & Search */}
            <div className="flex flex-col lg:flex-row gap-6 items-center justify-between">
                <div className="flex bg-white p-1.5 rounded-[1.5rem] shadow-sm border border-slate-100 w-full lg:w-auto">
                    {[
                        { id: "departments", label: "Program Studi", icon: PiGraduationCapBold },
                        { id: "skills", label: "Master Skills", icon: PiWrenchBold }
                    ].map(tab => (
                        <button 
                            key={tab.id}
                            onClick={() => { setActiveTab(tab.id); setSearchTerm(""); }}
                            className={`flex-1 lg:flex-none px-10 py-3.5 rounded-2xl text-sm font-extrabold transition-all flex items-center justify-center gap-2 ${activeTab === tab.id ? 'bg-sky-950 text-white shadow-lg shadow-sky-900/20' : 'text-slate-500 hover:text-sky-950 hover:bg-slate-50'}`}
                        >
                            <tab.icon size={20} />
                            {tab.label}
                        </button>
                    ))}
                </div>

                <div className="relative w-full lg:w-96 group">
                    <PiMagnifyingGlassBold className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-sky-600 transition-colors" />
                    <input 
                        type="text"
                        placeholder={`Cari ${activeTab === "departments" ? "prodi atau kode" : "nama skill atau kategori"}...`}
                        className="w-full pl-12 pr-4 py-4 bg-white border border-slate-100 rounded-2xl shadow-sm text-sm focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            {/* Content List */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {(loadingDepts || loadingSkills) ? (
                    <div className="lg:col-span-3 p-32 text-center text-slate-400 bg-white rounded-[2.5rem] border border-dashed border-slate-200">
                        <div className="flex flex-col items-center gap-4">
                            <div className="w-10 h-10 border-4 border-sky-100 border-t-sky-600 rounded-full animate-spin"></div>
                            <p className="font-bold tracking-widest uppercase text-xs">Mensinkronkan Data...</p>
                        </div>
                    </div>
                ) : filteredData?.length > 0 ? (
                    filteredData.map((item) => (
                        <div key={item.id} className="bg-white p-7 rounded-[2.5rem] shadow-sm border border-slate-100 hover:shadow-xl hover:border-sky-100 transition-all group flex flex-col justify-between relative overflow-hidden">
                            <div className="space-y-5">
                                <div className="flex justify-between items-start">
                                    <div className="p-4 bg-slate-50 rounded-2xl text-sky-950 shadow-inner group-hover:scale-110 transition-transform">
                                        {activeTab === "departments" ? <PiGraduationCapBold size={28} /> : <PiTagBold size={28} />}
                                    </div>
                                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
                                        <button onClick={() => handleEditClick(item)} className="p-3 text-slate-400 hover:text-sky-600 hover:bg-sky-50 rounded-xl transition-all shadow-sm border border-transparent hover:border-sky-100">
                                            <PiPencilSimpleBold size={20} />
                                        </button>
                                        <button onClick={() => handleDeleteClick(item)} className="p-3 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all shadow-sm border border-transparent hover:border-red-100">
                                            <PiTrashBold size={20} />
                                        </button>
                                    </div>
                                </div>
                                <div>
                                    <h3 className="font-extrabold text-slate-900 leading-tight text-lg tracking-tight">{item.name}</h3>
                                    {activeTab === "departments" ? (
                                        <div className="mt-3 space-y-1">
                                            <p className="text-[10px] font-extrabold text-sky-700 bg-sky-50 px-2 py-0.5 rounded inline-block uppercase tracking-wider">{item.code}</p>
                                            <p className="text-xs text-slate-400 font-bold block">{item.faculty}</p>
                                        </div>
                                    ) : (
                                        <div className="mt-3">
                                            <span className="bg-slate-50 text-slate-500 border border-slate-100 px-3 py-1 rounded-lg text-[10px] font-extrabold uppercase tracking-widest">
                                                {item.category || "Umum"}
                                            </span>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="lg:col-span-3 p-32 text-center text-slate-400 bg-white rounded-[2.5rem] border border-dashed border-slate-200 italic font-medium">
                        Tidak ada data master ditemukan.
                    </div>
                )}
            </div>

            {/* Form Modal */}
            {isFormOpen && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
                    <div className="absolute inset-0 bg-sky-950/60 backdrop-blur-md" onClick={() => setIsFormOpen(false)}></div>
                    <div className="relative bg-white rounded-[2.5rem] shadow-2xl w-full max-w-lg animate-in slide-in-from-bottom-10 duration-300 overflow-hidden">
                        <div className="p-10 border-b border-slate-100 flex justify-between items-center">
                            <h2 className="text-2xl font-extrabold text-slate-900">
                                {selectedItem ? `Edit ${activeTab === "departments" ? "Prodi" : "Skill"}` : `Tambah ${activeTab === "departments" ? "Prodi" : "Skill"}`}
                            </h2>
                            <button onClick={() => setIsFormOpen(false)} className="p-2 hover:bg-slate-50 rounded-2xl transition-all">
                                <PiXCircleFill size={32} className="text-slate-400" />
                            </button>
                        </div>
                        
                        <form onSubmit={handleSubmit} className="p-10 space-y-6">
                            <div className="space-y-2">
                                <label className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest">Nama {activeTab === "departments" ? "Program Studi" : "Skill"}</label>
                                <input 
                                    required
                                    className="w-full p-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-bold"
                                    value={formData.name || ""}
                                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                                />
                            </div>

                            {activeTab === "departments" ? (
                                <>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest">Kode Prodi</label>
                                        <input 
                                            required
                                            placeholder="Contoh: ILK"
                                            className="w-full p-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-bold"
                                            value={formData.code || ""}
                                            onChange={(e) => setFormData({...formData, code: e.target.value})}
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest">Fakultas</label>
                                        <input 
                                            required
                                            className="w-full p-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                            value={formData.faculty || ""}
                                            onChange={(e) => setFormData({...formData, faculty: e.target.value})}
                                        />
                                    </div>
                                </>
                            ) : (
                                <div className="space-y-2">
                                    <label className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest">Kategori Skill</label>
                                    <input 
                                        placeholder="Contoh: Programming, Design, etc."
                                        className="w-full p-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-sky-500/10 focus:border-sky-500 outline-none transition-all font-medium"
                                        value={formData.category || ""}
                                        onChange={(e) => setFormData({...formData, category: e.target.value})}
                                    />
                                </div>
                            )}

                            <button 
                                type="submit"
                                className="w-full py-5 bg-sky-950 text-white rounded-2xl font-extrabold shadow-xl shadow-sky-900/20 hover:bg-sky-900 transition-all active:scale-95"
                            >
                                {selectedItem ? "Simpan Perubahan" : "Simpan Data"}
                            </button>
                        </form>
                    </div>
                </div>
            )}

            <ConfirmModal 
                isOpen={isConfirmOpen}
                onClose={() => setIsConfirmOpen(false)}
                onConfirm={confirmDelete}
                title="Hapus Data Master?"
                message={`Anda akan menghapus "${itemToDelete?.name}". Data ini mungkin digunakan oleh profil mahasiswa atau lowongan aktif.`}
            />
        </div>
    );
}

export default AdminMasterData;
