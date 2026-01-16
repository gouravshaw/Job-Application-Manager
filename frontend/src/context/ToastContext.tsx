import React, { createContext, useContext, useState, useCallback } from 'react';
import { FaCheckCircle, FaExclamationCircle, FaInfoCircle, FaTimes } from 'react-icons/fa';

export type ToastType = 'success' | 'error' | 'info';

interface Toast {
      id: string;
      message: string;
      type: ToastType;
}

interface ToastContextType {
      showToast: (message: string, type: ToastType) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
      const [toasts, setToasts] = useState<Toast[]>([]);

      const showToast = useCallback((message: string, type: ToastType) => {
            const id = Math.random().toString(36).substr(2, 9);
            setToasts((prev) => [...prev, { id, message, type }]);

            setTimeout(() => {
                  setToasts((prev) => prev.filter((toast) => toast.id !== id));
            }, 4000);
      }, []);

      const removeToast = (id: string) => {
            setToasts((prev) => prev.filter((toast) => toast.id !== id));
      };

      return (
            <ToastContext.Provider value={{ showToast }}>
                  {children}
                  <div className="fixed bottom-4 right-4 z-[9999] flex flex-col gap-3 pointer-events-none">
                        {toasts.map((toast) => (
                              <div
                                    key={toast.id}
                                    className={`
              pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg border backdrop-blur-md transition-all duration-300 animate-slide-in-right
              ${toast.type === 'success'
                                                ? 'bg-emerald-50/90 dark:bg-emerald-900/40 border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200'
                                                : toast.type === 'error'
                                                      ? 'bg-red-50/90 dark:bg-red-900/40 border-red-200 dark:border-red-800 text-red-800 dark:text-red-200'
                                                      : 'bg-blue-50/90 dark:bg-blue-900/40 border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200'
                                          }
            `}
                              >
                                    <div className="text-lg">
                                          {toast.type === 'success' && <FaCheckCircle />}
                                          {toast.type === 'error' && <FaExclamationCircle />}
                                          {toast.type === 'info' && <FaInfoCircle />}
                                    </div>
                                    <p className="text-sm font-medium">{toast.message}</p>
                                    <button
                                          onClick={() => removeToast(toast.id)}
                                          className="ml-2 p-1 hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors"
                                    >
                                          <FaTimes className="text-xs opacity-70" />
                                    </button>
                              </div>
                        ))}
                  </div>
            </ToastContext.Provider>
      );
};

export const useToast = () => {
      const context = useContext(ToastContext);
      if (context === undefined) {
            throw new Error('useToast must be used within a ToastProvider');
      }
      return context;
};
