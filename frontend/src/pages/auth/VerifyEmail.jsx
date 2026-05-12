import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { PiSpinnerGap, PiCheckCircle, PiXCircle, PiArrowRight } from "react-icons/pi";

function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token");
  const { verifyEmail, isVerifying } = useAuth();
  const [status, setStatus] = useState("loading"); // loading, success, error
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setErrorMessage("Token verifikasi tidak ditemukan.");
      return;
    }

    const performVerification = async () => {
      // Tambahkan delay 1 detik agar transisi UI lebih halus
      await new Promise(resolve => setTimeout(resolve, 1000));
      try {
        await verifyEmail(token);
        setStatus("success");
        // Redirect after 3 seconds or user can click button
        setTimeout(() => {
          navigate("/login?verified=true");
        }, 3000);
      } catch (err) {
        setStatus("error");
        setErrorMessage(err.response?.data?.detail || "Gagal memverifikasi email.");
      }
    };

    performVerification();
  }, [token, verifyEmail, navigate]);

  return (
    <div className="h-screen w-full bg-[#F8FAFF] flex flex-col items-center justify-center p-6 font-jakarta">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl p-10 text-center space-y-6 border border-zinc-100">
        <div className="flex justify-center">
          <img src="/logo/laras.png" alt="LARAS" className="h-12 w-auto mb-4" />
        </div>

        {status === "loading" && (
          <div className="space-y-4">
            <div className="flex justify-center">
              <PiSpinnerGap size={64} className="text-[#002957] animate-spin" />
            </div>
            <h2 className="text-2xl font-bold text-[#002957]">Memverifikasi Email...</h2>
            <p className="text-zinc-500">Mohon tunggu sebentar, kami sedang memproses aktivasi akun Anda.</p>
          </div>
        )}

        {status === "success" && (
          <div className="space-y-4">
            <div className="flex justify-center text-green-500">
              <PiCheckCircle size={80} weight="fill" />
            </div>
            <h2 className="text-2xl font-bold text-[#002957]">Email Terverifikasi!</h2>
            <p className="text-zinc-500 font-medium">
              Akun Anda telah berhasil diaktifkan. Anda akan diarahkan ke halaman login dalam beberapa detik.
            </p>
            <button
              onClick={() => navigate("/login?verified=true")}
              className="w-full py-4 bg-[#002957] text-white rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-[#001f42] transition-all"
            >
              <span>Masuk Sekarang</span>
              <PiArrowRight size={20} weight="bold" />
            </button>
          </div>
        )}

        {status === "error" && (
          <div className="space-y-4">
            <div className="flex justify-center text-red-500">
              <PiXCircle size={80} weight="fill" />
            </div>
            <h2 className="text-2xl font-bold text-[#002957]">Verifikasi Gagal</h2>
            <p className="text-red-600 font-medium bg-red-50 p-4 rounded-xl border border-red-100">
              {errorMessage}
            </p>
            <button
              onClick={() => navigate("/registration")}
              className="w-full py-4 bg-[#002957] text-white rounded-xl font-bold hover:bg-[#001f42] transition-all"
            >
              Kembali ke Registrasi
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default VerifyEmail;
