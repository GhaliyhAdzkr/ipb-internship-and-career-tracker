import { PiWarningCircleFill, PiXBold } from 'react-icons/pi';

const ConfirmModal = ({ isOpen, onClose, onConfirm, title, message, confirmText = "Hapus", cancelText = "Batal", type = "danger" }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      {/* Latar Belakang */}
      <div 
        className="absolute inset-0 bg-sky-950/40 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      ></div>

      {/* Konten Modal */}
      <div className="relative bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">

        <div className="p-8">
          <div className="flex justify-between items-start mb-6">
            <div className={`p-3 rounded-2xl ${type === 'danger' ? 'bg-red-50 text-red-600' : 'bg-amber-50 text-amber-600'}`}>
              <PiWarningCircleFill size={32} />
            </div>
            <button 
              onClick={onClose}
              className="p-2 hover:bg-slate-50 rounded-xl transition-colors text-slate-400"
            >
              <PiXBold size={20} />
            </button>
          </div>

          <h3 className="text-xl font-bold text-slate-900 mb-2">{title}</h3>
          <p className="text-slate-500 text-sm leading-relaxed">
            {message}
          </p>
        </div>

        <div className="px-8 py-6 bg-slate-50 flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-6 py-3 rounded-2xl font-bold text-slate-600 hover:bg-slate-100 transition-all text-sm"
          >
            {cancelText}
          </button>
          <button
            onClick={() => {
              onConfirm();
              onClose();
            }}
            className={`flex-1 px-6 py-3 rounded-2xl font-bold text-white transition-all text-sm shadow-lg ${
              type === 'danger' 
              ? 'bg-red-600 hover:bg-red-700 shadow-red-200' 
              : 'bg-sky-950 hover:bg-sky-900 shadow-sky-200'
            }`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmModal;
