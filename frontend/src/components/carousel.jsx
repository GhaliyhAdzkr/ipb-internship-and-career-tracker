import { Swiper, SwiperSlide, useSwiper } from 'swiper/react';
import { Pagination } from 'swiper/modules';

// Pembuatan komponen untuk tombol navigasi
const SwiperNavButtons = () => {
  const swiper = useSwiper();

  return (
    <div className="swiper-nav-btns">
      <button onClick={() => swiper.slidePrev()}>Prev</button>
      <button onClick={() => swiper.slideNext()}>Next</button>
    </div>
  );
};

export default function App() {
  return (
    <Swiper
      modules={[Pagination]} // Modul navigasi tidak terlalu dibutuhkan di sini
      spaceBetween={45}
      slidesPerView={5}
      pagination={{ clickable: true }}
    >
      {/* Letakkan tombol navigasi di dalam komponen Swiper */}
      <SwiperNavButtons />

      <SwiperSlide>Slide 1</SwiperSlide>
      <SwiperSlide>Slide 2</SwiperSlide>
      <SwiperSlide>Slide 3</SwiperSlide>
    </Swiper>
  );
}