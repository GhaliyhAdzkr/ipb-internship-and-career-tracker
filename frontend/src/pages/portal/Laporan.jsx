import { useState } from "react";
import { 
  PiFileText, PiCheckCircle, PiSpinner, PiDownloadSimple, 
  PiArrowClockwise, PiWarning, PiClock, PiEnvelopeSimple,
  PiCheckCircleFill, PiListBullets
} from "react-icons/pi";
import { format } from "date-fns";
import { id } from "date-fns/locale";
import toast from "react-hot-toast";
import { usePlacements, useReport } from "../../hooks/usePlacements";
import { useDocuments } from "../../hooks/useDocuments";

const DOCUMENT_TYPES = [
  { value: "SURAT_PENGANTAR", label: "Surat Pengantar Magang" },
  { value: "SURAT_REKOMENDASI", label: "Surat Rekomendasi" },
];

const STATUS_CONFIG = {
  PENDING:    { label: "Diproses",    className: "bg-amber-100 text-amber-800" },
  PROCESSING: { label: "Sedang Dibuat", className: "bg-sky-100 text-sky-800" },
  COMPLETED:  { label: "Selesai",     className: "bg-emerald-100 text-emerald-800" },
  FAILED:     { label: "Gagal",       className: "bg-rose-100 text-rose-800" },
};

// Bagian Permohonan Dokumen

function DocumentSection() {
  const { documents, isLoading, requestDocument, isRequesting, requestError } = useDocuments();
  const [docType, setDocType] = useState(DOCUMENT_TYPES[0].value);
  const [purpose, setPurpose] = useState("");
  const [showForm, setShowForm] = useState(false);

  const handleRequest = async (e) => {
    e.preventDefault();
    if (!purpose.trim()) { toast.error("Keperluan surat wajib diisi."); return; }
    try {
      const result = await requestDocument({ document_type: docType, purpose });
      toast.success(result.message || "Permohonan berhasil diajukan.");
      setPurpose("");
      setShowForm(false);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Gagal mengajukan permohonan.");
    }
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Form Pengajuan */}
      {showForm ? (
        <div className="p-6 bg-white rounded-xl shadow-sm border border-slate-100">
          <h3 className="font-bold text-slate-800 text-base mb-4 border-b border-slate-100 pb-3 flex items-center gap-2">
            <PiEnvelopeSimple size={20} className="text-sky-700" />
            Ajukan Permohonan Surat
          </h3>
          <form onSubmit={handleRequest} className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-bold text-slate-700">Jenis Surat</label>
              <select
                value={docType}
                onChange={(e) => setDocType(e.target.value)}
                className="w-full py-2.5 px-3 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 outline-none transition-all"
              >
                {DOCUMENT_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-bold text-slate-700">Keperluan</label>
              <textarea
                value={purpose}
                onChange={(e) => setPurpose(e.target.value)}
                placeholder="Contoh: Melamar magang di PT ABC sebagai Software Engineer"
                rows={3}
                className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 outline-none resize-none transition-all"
              />
            </div>
            {requestError && (
              <p className="text-xs text-rose-600 font-bold">
                {requestError.response?.data?.detail || "Terjadi kesalahan."}
              </p>
            )}
            <div className="flex gap-3 justify-end pt-2">
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-4 py-2 text-slate-600 font-bold text-sm hover:bg-slate-100 rounded-lg transition-colors"
              >Batal</button>
              <button
                type="submit"
                disabled={isRequesting}
                className="flex items-center gap-2 px-6 py-2 bg-sky-950 text-white font-bold rounded-lg text-sm hover:bg-sky-900 transition-all disabled:opacity-70"
              >
                {isRequesting && <PiSpinner className="animate-spin" size={16} />}
                Ajukan
              </button>
            </div>
          </form>
        </div>
      ) : (
        <div className="flex justify-end">
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 px-5 py-2.5 bg-sky-950 text-white font-bold rounded-lg text-sm hover:bg-sky-900 transition-all shadow-md"
          >
            <PiEnvelopeSimple size={18} /> Ajukan Surat Baru
          </button>
        </div>
      )}

      {/* Riwayat Pengajuan */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
        <div className="flex items-center gap-2 px-6 py-4 border-b border-slate-100">
          <PiListBullets size={20} className="text-sky-700" />
          <h3 className="font-bold text-slate-800">Riwayat Permohonan</h3>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center gap-3 py-12 text-slate-500">
            <PiSpinner className="animate-spin" size={24} />
            <span className="text-sm font-bold">Memuat riwayat...</span>
          </div>
        ) : documents.length === 0 ? (
          <div className="text-center py-14 flex flex-col items-center gap-3">
            <PiEnvelopeSimple size={48} className="text-zinc-200" />
            <p className="font-bold text-slate-500 text-sm">Belum ada permohonan surat.</p>
          </div>
        ) : (
          <div className="divide-y divide-slate-50">
            {documents.map((doc) => {
              const status = STATUS_CONFIG[doc.status] || { label: doc.status, className: "bg-slate-100 text-slate-700" };
              return (
                <div key={doc.id} className="px-6 py-4 flex items-center justify-between gap-4 hover:bg-slate-50/50 transition-colors">
                  <div className="flex flex-col gap-1 min-w-0">
                    <p className="font-bold text-slate-800 text-sm truncate">
                      {DOCUMENT_TYPES.find((t) => t.value === doc.document_type)?.label || doc.document_type}
                    </p>
                    <p className="text-xs text-slate-500 truncate">{doc.purpose}</p>
                    <p className="text-[11px] text-slate-400">
                      {format(new Date(doc.created_at), "d MMM yyyy, HH:mm", { locale: id })}
                    </p>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <span className={`text-[10px] font-bold px-2.5 py-1 rounded uppercase ${status.className}`}>
                      {status.label}
                    </span>
                    {doc.status === "COMPLETED" && doc.generated_url && (
                      <a
                        href={doc.generated_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 text-xs text-sky-700 font-bold hover:underline"
                      >
                        <PiDownloadSimple size={16} /> Unduh
                      </a>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

// Bagian Laporan Akhir

function ReportSection({ activePlacement }) {
  const { report, isLoadingReport, generateReport, isGenerating, generateError } = useReport(activePlacement?.id);

  const handleGenerate = async () => {
    try {
      const result = await generateReport();
      toast.success(result.message || "Proses pembuatan laporan dimulai.");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Gagal memulai pembuatan laporan.");
    }
  };

  const isGenerated = report?.status === "generated";
  const isProcessing = report?.status === "processing";

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Sisi Kiri: Informasi Penempatan */}
      <div className="lg:col-span-1 flex flex-col gap-4">
        <div className="p-6 bg-white rounded-xl shadow-sm border border-slate-100 flex flex-col gap-5">
          <h3 className="font-bold text-slate-800 border-b border-slate-100 pb-3">Detail Penempatan</h3>
          <dl className="space-y-3 text-sm">
            <div>
              <dt className="text-xs text-slate-500 font-medium">Perusahaan</dt>
              <dd className="font-bold text-slate-800 mt-0.5">{activePlacement?.company_name || "–"}</dd>
            </div>
            <div>
              <dt className="text-xs text-slate-500 font-medium">Periode</dt>
              <dd className="font-bold text-slate-800 mt-0.5">
                {activePlacement ? (
                  `${format(new Date(activePlacement.start_date), "dd MMM yyyy", { locale: id })} s/d ${format(new Date(activePlacement.end_date), "dd MMM yyyy", { locale: id })}`
                ) : (
                  "–"
                )}
              </dd>
            </div>
            {activePlacement?.external_supervisor_name && (
              <div>
                <dt className="text-xs text-slate-500 font-medium">Pembimbing Lapangan</dt>
                <dd className="font-bold text-slate-800 mt-0.5">{activePlacement.external_supervisor_name}</dd>
              </div>
            )}
          </dl>
        </div>

        <div className="p-6 bg-white rounded-xl shadow-sm border border-slate-100 flex flex-col gap-4">
          <h3 className="font-bold text-slate-800 border-b border-slate-100 pb-3">Syarat Generate</h3>
          <ul className="space-y-3">
            {["Masa magang telah selesai", "Jurnal harian telah diisi", "Tunggu maksimal 5 menit setelah generate"].map((text, i) => (
              <li key={i} className="flex items-start gap-3">
                <PiCheckCircle size={18} className="text-emerald-500 mt-0.5 shrink-0" />
                <span className="text-sm text-zinc-600">{text}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Sisi Kanan: Status Laporan Akhir */}
      <div className="lg:col-span-2 h-full">
        <div className="h-full p-5 sm:p-8 bg-white rounded-xl shadow-sm border border-slate-100 flex flex-col gap-6">
          <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
            <PiFileText size={24} className="text-sky-950" />
            <h3 className="text-lg font-bold text-slate-800">Status Laporan</h3>
          </div>

          {isLoadingReport ? (
            <div className="flex items-center gap-3 py-8 justify-center text-slate-500">
              <PiSpinner className="animate-spin" size={24} />
              <span className="font-bold text-sm">Mengambil status laporan...</span>
            </div>
          ) : !activePlacement ? (
            <div className="flex items-center gap-4 p-5 bg-slate-50 rounded-xl border border-slate-100">
              <PiWarning size={28} className="text-amber-500 shrink-0" />
              <p className="font-bold text-slate-700 text-sm">Belum ada penempatan aktif. Laporan belum tersedia.</p>
            </div>
          ) : isGenerated ? (
            <div className="flex flex-col gap-5">
              <div className="flex items-center gap-4 p-5 bg-emerald-50 text-emerald-800 rounded-xl border border-emerald-100">
                <PiCheckCircleFill size={32} className="shrink-0" />
                <div>
                  <p className="font-bold text-base">Laporan Siap Diunduh</p>
                  <p className="text-sm opacity-80 mt-0.5">Laporan otomatis Anda telah berhasil digenerate.</p>
                </div>
              </div>
              <div className="flex gap-3 justify-end">
                <button
                  onClick={handleGenerate}
                  disabled={isGenerating}
                  className="flex items-center gap-2 px-4 py-2.5 border border-slate-200 text-slate-600 font-bold rounded-lg text-sm hover:bg-slate-50 transition-colors"
                >
                  <PiArrowClockwise size={18} /> Generate Ulang
                </button>
                <a
                  href={report?.auto_generated_report_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-6 py-2.5 bg-sky-950 text-white font-bold rounded-lg text-sm hover:bg-sky-900 transition-colors shadow-md"
                >
                  <PiDownloadSimple size={18} /> Unduh Laporan
                </a>
              </div>
            </div>
          ) : isProcessing ? (
            <div className="flex flex-col items-center gap-4 py-10 text-center">
              <div className="relative">
                <PiClock size={52} className="text-sky-100" />
                <PiSpinner size={20} className="animate-spin text-sky-600 absolute -bottom-1 -right-1" />
              </div>
              <p className="font-bold text-slate-700">Laporan sedang diproses...</p>
              <p className="text-sm text-slate-500 max-w-sm">
                Sistem sedang menyusun laporan. Halaman ini otomatis diperbarui setiap 30 detik.
              </p>
            </div>
          ) : (
            <div className="flex flex-col gap-5">
              <div className="flex items-center gap-4 p-5 bg-amber-50 text-amber-800 rounded-xl border border-amber-100">
                <PiFileText size={32} className="shrink-0" />
                <div>
                  <p className="font-bold text-base">Laporan Belum Digenerate</p>
                  <p className="text-sm opacity-80 mt-0.5">Klik tombol di bawah untuk membuat laporan akhir otomatis dari jurnal Anda.</p>
                </div>
              </div>
              {generateError && (
                <div className="flex items-start gap-3 p-4 bg-rose-50 text-rose-700 rounded-lg border border-rose-100 text-sm">
                  <PiWarning size={20} className="shrink-0 mt-0.5" />
                  <span>{generateError.response?.data?.detail || "Terjadi kesalahan."}</span>
                </div>
              )}
              <div className="flex justify-end">
                <button
                  onClick={handleGenerate}
                  disabled={isGenerating}
                  className="flex items-center gap-2 px-8 py-3 bg-sky-950 text-white font-bold rounded-lg hover:bg-sky-900 transition-all shadow-md hover:shadow-lg disabled:opacity-70"
                >
                  {isGenerating
                    ? <><PiSpinner className="animate-spin" size={18} /> Memproses...</>
                    : <><PiArrowClockwise size={18} /> Generate Laporan Otomatis</>
                  }
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Root Halaman Laporan dan Dokumen

const TABS = [
  { id: "laporan", label: "Laporan Akhir", icon: PiFileText },
  { id: "dokumen", label: "Surat & Dokumen", icon: PiEnvelopeSimple },
];

function Laporan() {
  const [activeTab, setActiveTab] = useState("laporan");
  const { data: placements = [], isLoading: isLoadingPlacements } = usePlacements();
  const activePlacement = placements[0] || null;

  if (isLoadingPlacements) {
    return (
      <div className="h-full flex items-center justify-center">
        <PiSpinner className="animate-spin text-sky-950" size={40} />
      </div>
    );
  }

  return (
    <div className="font-jakarta">
      {/* Banner Utama */}
      <div className="mb-6 bg-sky-950 py-6 px-5 sm:py-7 sm:px-10 rounded-xl text-white shadow-[0px_8px_24px_0px_rgba(0,41,87,0.06)] relative overflow-hidden">
        <div className="relative z-10">
          <div className="text-2xl sm:text-3xl font-bold">Laporan & Dokumen</div>
          <div className="text-sm sm:text-base opacity-90 mt-2 max-w-2xl">
            Generate laporan akhir internship dan ajukan permohonan surat pengantar secara otomatis.
          </div>
        </div>
        <div className="absolute top-0 right-0 w-64 h-64 bg-sky-900 rounded-full blur-3xl opacity-50 -translate-y-10 translate-x-10" />
      </div>

      {/* Tab Navigasi */}
      <div className="flex gap-1 mb-6 bg-white p-1.5 rounded-xl shadow-sm border border-slate-100 w-full sm:w-fit overflow-x-auto">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === tab.id
                ? "bg-sky-950 text-white shadow-md"
                : "text-slate-500 hover:text-sky-800 hover:bg-sky-50"
            }`}
          >
            <tab.icon size={18} />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Konten Aktif */}
      {activeTab === "laporan" ? (
        <ReportSection activePlacement={activePlacement} />
      ) : (
        <DocumentSection />
      )}
    </div>
  );
}

export default Laporan;
