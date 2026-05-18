import React from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { 
    PiUsersThin, 
    PiBriefcaseThin, 
    PiBuildingsThin, 
    PiCheckCircleThin,
    PiClockThin
} from "react-icons/pi";
import adminService from "../../services/adminService";
import { useAuth } from "../../hooks/useAuth";

function AdminDashboard() {
    const { user } = useAuth();
    
    // Fetch statistics/data for dashboard
    const { data: pendingApplications, isLoading: loadingApps } = useQuery({
        queryKey: ["admin", "pending-verifications"],
        queryFn: adminService.getPendingVerifications
    });

    const { data: companies } = useQuery({
        queryKey: ["admin", "companies"],
        queryFn: adminService.getCompanies
    });

    const stats = [
        { 
            label: "Verifikasi Tertunda", 
            value: pendingApplications?.length || 0, 
            icon: PiClockThin, 
            color: "text-amber-600",
            bg: "bg-amber-50" 
        },
        { 
            label: "Total Perusahaan", 
            value: companies?.length || 0, 
            icon: PiBuildingsThin, 
            color: "text-sky-600",
            bg: "bg-sky-50" 
        },
        { 
            label: "Lowongan Aktif", 
            value: "10", // Placeholder for now
            icon: PiBriefcaseThin, 
            color: "text-emerald-600",
            bg: "bg-emerald-50" 
        },
        { 
            label: "Total Mahasiswa", 
            value: "142", // Placeholder for now
            icon: PiUsersThin, 
            color: "text-indigo-600",
            bg: "bg-indigo-50" 
        }
    ];

    return (
        <div className="font-jakarta space-y-8">
            {/* Header / Welcome Area */}
            <div className="bg-sky-950 py-10 px-10 rounded-[2.5rem] text-white shadow-xl relative overflow-hidden">
                <div className="relative z-10">
                    <h1 className="text-3xl font-bold mb-2">Panel Administrator CDA</h1>
                    <p className="text-sky-200 max-w-xl">
                        Selamat datang kembali, {user?.full_name || 'Admin'}. Kelola data master, verifikasi dokumen, dan pantau aktivitas karir mahasiswa IPB di sini.
                    </p>
                </div>
                {/* Decorative background element */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -mr-20 -mt-20 blur-3xl"></div>
            </div>

            {/* Statistics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, idx) => (
                    <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex items-center gap-5 transition-all hover:shadow-md">
                        <div className={`${stat.bg} ${stat.color} p-4 rounded-xl`}>
                            <stat.icon size={28} weight="thin" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-slate-500">{stat.label}</p>
                            <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Main Content Areas */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Verification Queue Preview */}
                <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden text-sm">
                    <div className="p-6 border-b border-slate-50 flex justify-between items-center">
                        <h2 className="font-bold text-slate-900 text-lg">Verifikasi Perlu Tindakan</h2>
                        <button className="text-sky-700 font-bold hover:underline">Lihat Semua</button>
                    </div>
                    <div className="divide-y divide-slate-50">
                        {loadingApps ? (
                            <div className="p-10 text-center text-slate-400">Memuat antrean...</div>
                        ) : pendingApplications?.length > 0 ? (
                            pendingApplications.slice(0, 5).map((app) => (
                                <div key={app.id} className="p-4 hover:bg-slate-50 flex justify-between items-center transition-colors">
                                    <div className="flex gap-4 items-center">
                                        <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-600">
                                            {app.student?.user?.full_name?.charAt(0)}
                                        </div>
                                        <div>
                                            <p className="font-bold text-slate-900">{app.student?.user?.full_name}</p>
                                            <p className="text-slate-500 text-xs">{app.vacancy?.title} • {app.vacancy?.company?.name}</p>
                                        </div>
                                    </div>
                                    <button className="bg-sky-950 text-white px-4 py-2 rounded-lg font-bold text-xs hover:bg-sky-900">
                                        Periksa
                                    </button>
                                </div>
                            ))
                        ) : (
                            <div className="p-10 text-center text-slate-400">Tidak ada antrean verifikasi saat ini.</div>
                        )}
                    </div>
                </div>

                {/* Quick Actions / Master Data Summary */}
                <div className="space-y-6">
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 italic text-slate-500 text-sm">
                        &ldquo;Efisienkan proses administrasi untuk mempercepat karir mahasiswa IPB.&rdquo;
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                        <Link 
                            to="/app/admin/perusahaan"
                            className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:border-sky-200 hover:bg-sky-50 transition-all flex flex-col items-center gap-3"
                        >
                            <PiBuildingsThin size={32} className="text-sky-900" />
                            <span className="font-bold text-slate-900">Kelola PT</span>
                        </Link>
                        <Link 
                            to="/app/admin/verifikasi"
                            className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:border-sky-200 hover:bg-sky-50 transition-all flex flex-col items-center gap-3"
                        >
                            <PiCheckCircleThin size={32} className="text-sky-900" />
                            <span className="font-bold text-slate-900">Validasi</span>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AdminDashboard;