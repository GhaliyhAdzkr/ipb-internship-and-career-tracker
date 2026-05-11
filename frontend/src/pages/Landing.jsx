import React from 'react';
import { Link } from 'react-router-dom';
import Lowongan from './Lowongan';

export default function Landing() {
  return (
    <div className="font-jakarta text-sky-950">
      <nav className="bg-white border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link to="/" className="flex items-center gap-3">
              <img src="/logo/laras.png" alt="LARAS IPB" className="w-28 h-auto object-contain" />
            </Link>
            <div className="hidden md:flex items-center gap-6 text-sm">
              <Link to="/" className="font-medium hover:text-sky-700">Beranda</Link>
              <Link to="/lowongan" className="font-medium hover:text-sky-700">Lowongan</Link>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:block">
              <input
                aria-label="search"
                className="w-64 py-2 px-3 rounded-full bg-zinc-50 border border-zinc-100 text-sm outline-none focus:ring-2 focus:ring-sky-200"
                placeholder="Cari lowongan..."
              />
            </div>
            <Link to="/login" className="text-sm px-4 py-2">Masuk</Link>
            <Link to="/registration" className="bg-sky-950 text-white px-4 py-2 rounded-md text-sm">Daftar</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <header className="relative bg-[url('/assets/hero-campus.jpg')] bg-center bg-cover">
        <div className="absolute inset-0 bg-white/70 backdrop-blur-sm"></div>
        <div className="relative max-w-7xl mx-auto px-6 py-20">
          <div className="grid lg:grid-cols-2 gap-8 items-center">
            <div>
              <p className="text-sm text-sky-800 font-semibold mb-3">Portal Resmi IPB University</p>
              <h1 className="text-4xl md:text-5xl font-extrabold leading-tight text-sky-950 mb-4">Bangun Karier <span className="text-sky-600">Profesional Anda</span></h1>
              <p className="text-base text-zinc-700 max-w-xl mb-8">Platform magang dan rekrutmen terintegrasi untuk mahasiswa dan alumni IPB University. Temukan peluang dari mitra industri terbaik.</p>

              <div className="bg-white rounded-xl p-4 shadow-lg w-full max-w-2xl">
                <div className="flex gap-3 items-center">
                  <input placeholder="Posisi atau perusahaan" className="flex-1 py-3 px-4 rounded-lg border border-zinc-100 outline-none" />
                  <input placeholder="Lokasi" className="w-44 py-3 px-4 rounded-lg border border-zinc-100 outline-none" />
                  <button className="bg-sky-950 text-white px-6 py-3 rounded-lg font-bold">Cari</button>
                </div>
                <div className="mt-3 text-xs text-zinc-500">Pencarian populer: <span className="text-sky-700 font-medium">Data Analyst</span> · <span className="text-sky-700 font-medium">Agronomi</span> · <span className="text-sky-700 font-medium">Management Trainee</span></div>
              </div>
            </div>

            <div className="hidden lg:block">
              {/* Decorative right column to match design */}
              <div className="h-72 bg-white/60 rounded-xl shadow-inner flex items-center justify-center">
                <div className="text-center text-sky-700 font-bold">Hero Illustration</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12">
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">Temukan karir yang sesuai dengan anda</h2>
          <p className="text-sm text-zinc-500 mb-6">Rekomendasi lowongan magang terbaru untuk Anda.</p>
          <Lowongan />
        </section>

        <section className="mt-16 text-center text-zinc-500">
          <div className="uppercase text-xs tracking-wider mb-6">Bergabung bersama perusahaan terbaik</div>
          <div className="flex items-center justify-center gap-12 opacity-60">
            <div className="w-32 h-10 bg-zinc-100 rounded-md"></div>
            <div className="w-32 h-10 bg-zinc-100 rounded-md"></div>
            <div className="w-32 h-10 bg-zinc-100 rounded-md"></div>
            <div className="w-32 h-10 bg-zinc-100 rounded-md"></div>
          </div>
        </section>
      </main>
    </div>
  );
}
