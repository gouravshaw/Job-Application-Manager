import { useEffect } from 'react';

interface KeyboardShortcutHandlers {
  onNewApplication?: () => void;
  onSearch?: () => void;
  onEscape?: () => void;
  onToggleDarkMode?: () => void;
}

export const useKeyboardShortcuts = (handlers: KeyboardShortcutHandlers) => {
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      // Don't trigger shortcuts when typing in inputs
      const target = event.target as HTMLElement;
      const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA';
      
      // Escape key - works everywhere
      if (event.key === 'Escape' && handlers.onEscape) {
        handlers.onEscape();
        return;
      }

      // Skip if typing in an input (except for Escape)
      if (isInput) return;

      // Ctrl/Cmd + K or just '/' for search
      if (((event.ctrlKey || event.metaKey) && event.key === 'k') || event.key === '/') {
        event.preventDefault();
        if (handlers.onSearch) {
          handlers.onSearch();
        }
      }

      // 'n' for new application
      if (event.key === 'n' || event.key === 'N') {
        event.preventDefault();
        if (handlers.onNewApplication) {
          handlers.onNewApplication();
        }
      }

      // 'd' for toggle dark mode
      if (event.key === 'd' && event.shiftKey) {
        event.preventDefault();
        if (handlers.onToggleDarkMode) {
          handlers.onToggleDarkMode();
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handlers]);
};

