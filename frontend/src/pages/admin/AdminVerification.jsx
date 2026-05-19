import { useState } from "react";
import { 
    PiCheckCircleFill, 
    PiXCircleFill, 
    PiFilePdfFill,
    PiEyeFill,
    PiClockFill
} from "react-icons/pi";
import { useAdminVerification } from "../../hooks/useAdminVerification";

function AdminVerification() {
    const [selectedApp, setSelectedApp] = useState(null);
    const [remarks, setRemarks] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    const {
        applications,
        isLoadingApplications: isLoading,
        verifyMutation,
        rejectMutation
    } = useAdminVerification(() => {
        setSelectedApp(null);
        setRemarks("");
        setStartDate("");
        setEndDate("");
    });

    const handleVerify = (id) => {
        if (!startDate || !endDate) {
            alert("Harap isi tanggal mulai dan tanggal selesai penempatan.");
            return;
        }
        verifyMutation.mutate({ id, data: { start_date: startDate, end_date: endDate } });
    };

    const handleReject = (id) => {
        if (!remarks) {
            alert("Harap isi alasan penolakan pada catatan.");
            return;
        }
        rejectMutation.mutate({ id, data: { reason: remarks } });
    };

    return (
        <div className="font-jakarta space-y-8 pb-20">
            {/* Header Banner */}
            <div className="bg-sky-950 py-12 px-10 rounded-[2.5rem] text-white shadow-xl relative overflow-hidden">
                <div className="relative z-10">
                    <h1 className="text-3xl font-extrabold mb-2 tracking-tight">Verifikasi Lamaran</h1>
                    <p className="text-sky-200 max-w-xl text-lg opacity-80 font-medium leading-relaxed">
                        Tinjau dokumen pendukung dan syarat lamaran mahasiswa. Pastikan semua data valid sebelum menyetujui penempatan magang.
                    </p>
                    <div className="mt-8 inline-flex bg-white/10 backdrop-blur-md px-6 py-3 rounded-2xl text-sm font-bold items-center gap-3 border border-white/10 shadow-lg shadow-sky-900/20">
                        <PiClockFill className="text-amber-400" size={20} />
                        <span>{applications?.length || 0} Perlu Diverifikasi</span>
                    </div>
                </div>
                <div className="absolute top-0 right-0 w-96 h-96 bg-white/5 rounded-full -mr-32 -mt-32 blur-[100px]"></div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* List Area */}
                <div className="lg:col-span-2 space-y-4">
                    {isLoading ? (
                        <div className="p-10 text-center text-slate-400 bg-white rounded-2xl border border-slate-100 italic">
                            Memuat daftar lamaran...
                        </div>
                    ) : applications?.length > 0 ? (
                        applications.map((app) => (
                            <div 
                                key={app.id} 
                                onClick={() => setSelectedApp(app)}
                                className={`p-5 bg-white rounded-2xl border transition-all cursor-pointer flex justify-between items-center ${
                                    selectedApp?.id === app.id ? 'border-sky-500 shadow-md ring-1 ring-sky-500/20' : 'border-slate-100 hover:border-sky-200 shadow-sm'
                                }`}
                            >
                                <div className="flex gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-sky-50 text-sky-700 flex items-center justify-center font-bold text-lg">
                                        {app.student?.user?.full_name?.charAt(0)}
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-slate-900">{app.student?.user?.full_name}</h3>
                                        <p className="text-slate-500 text-xs">{app.vacancy?.title} • {app.vacancy?.company?.name}</p>
                                        <div className="mt-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                                            Diunggah: {new Date(app.created_at).toLocaleDateString('id-ID')}
                                        </div>
                                    </div>
                                </div>
                                <PiEyeFill size={20} className={selectedApp?.id === app.id ? 'text-sky-500' : 'text-slate-300'} />
                            </div>
                        ))
                    ) : (
                        <div className="p-10 text-center text-slate-400 bg-white rounded-2xl border border-slate-100 italic">
                            Belum ada lamaran yang perlu diverifikasi.
                        </div>
                    )}
                </div>

                {/* Detail/Action Area */}
                <div className="lg:col-span-1">
                    {selectedApp ? (
                        <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 sticky top-6 space-y-6">
                            <h2 className="font-bold text-slate-900 text-lg border-b pb-4">Dokumen Pendukung</h2>
                            
                            <div className="space-y-3">
                                <a 
                                    href={selectedApp.cv_url} 
                                    target="_blank" 
                                    rel="noreferrer"
                                    className="flex items-center gap-3 p-3 rounded-xl bg-slate-50 hover:bg-slate-100 transition-colors group"
                                >
                                    <PiFilePdfFill className="text-red-500" size={24} />
                                    <div className="flex-1">
                                        <p className="text-sm font-bold text-slate-900">Curriculum Vitae</p>
                                        <p className="text-[10px] text-slate-500 uppercase">Klik untuk pratinjau</p>
                                    </div>
                                </a>
                                {selectedApp.portfolio_url && (
                                    <a 
                                        href={selectedApp.portfolio_url} 
                                        target="_blank" 
                                        rel="noreferrer"
                                        className="flex items-center gap-3 p-3 rounded-xl bg-slate-50 hover:bg-slate-100 transition-colors group"
                                    >
                                        <PiFilePdfFill className="text-sky-500" size={24} />
                                        <div className="flex-1">
                                            <p className="text-sm font-bold text-slate-900">Portfolio</p>
                                            <p className="text-[10px] text-slate-500 uppercase tracking-widest">Klik untuk pratinjau</p>
                                        </div>
                                    </a>
                                )}
                                {selectedApp.proof_url && (
                                    <a
                                        href={selectedApp.proof_url}
                                        target="_blank"
                                        rel="noreferrer"
                                        className="flex items-center gap-3 p-3 rounded-xl bg-emerald-50 hover:bg-emerald-100 transition-colors group border border-emerald-100"
                                    >
                                        <PiFilePdfFill className="text-emerald-600" size={24} />
                                        <div className="flex-1">
                                            <p className="text-sm font-bold text-slate-900">Bukti LoA / Penerimaan</p>
                                            <p className="text-[10px] text-slate-500 uppercase">Klik untuk pratinjau</p>
                                        </div>
                                    </a>
                                )}
                            </div>

                            <div className="space-y-3">
                                <label className="text-xs font-bold text-slate-500 uppercase">Periode Penempatan</label>
                                <div className="grid grid-cols-2 gap-3">
                                    <div>
                                        <span className="text-[10px] font-bold text-slate-400 uppercase">Mulai</span>
                                        <input
                                            type="date"
                                            value={startDate}
                                            onChange={(e) => setStartDate(e.target.value)}
                                            className="mt-1 w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-sky-500 outline-none"
                                        />
                                    </div>
                                    <div>
                                        <span className="text-[10px] font-bold text-slate-400 uppercase">Selesai</span>
                                        <input
                                            type="date"
                                            value={endDate}
                                            min={startDate || undefined}
                                            onChange={(e) => setEndDate(e.target.value)}
                                            className="mt-1 w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-sky-500 outline-none"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-3">
                                <label className="text-xs font-bold text-slate-500 uppercase">Catatan Verifikasi</label>
                                <textarea 
                                    className="w-full p-4 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-sky-500 outline-none h-32"
                                    placeholder="Tambahkan catatan untuk mahasiswa..."
                                    value={remarks}
                                    onChange={(e) => setRemarks(e.target.value)}
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-3 pt-4">
                                <button 
                                    onClick={() => handleReject(selectedApp.id)}
                                    disabled={rejectMutation.isPending || verifyMutation.isPending}
                                    className="flex items-center justify-center gap-2 py-3 bg-white border border-red-200 text-red-600 font-bold rounded-xl hover:bg-red-50 transition-colors disabled:opacity-50"
                                >
                                    <PiXCircleFill size={20} />
                                    Tolak
                                </button>
                                <button 
                                    onClick={() => handleVerify(selectedApp.id)}
                                    disabled={rejectMutation.isPending || verifyMutation.isPending}
                                    className="flex items-center justify-center gap-2 py-3 bg-emerald-600 text-white font-bold rounded-xl hover:bg-emerald-700 transition-colors shadow-lg shadow-emerald-200 disabled:opacity-50"
                                >
                                    <PiCheckCircleFill size={20} />
                                    Terima
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="bg-slate-50 rounded-2xl border border-dashed border-slate-200 p-10 text-center text-slate-400 text-sm italic">
                            Pilih lamaran dari daftar untuk melihat detail verifikasi.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default AdminVerification;
