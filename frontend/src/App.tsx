import { useState } from 'react';
import { FaBriefcase, FaChartBar, FaMoon, FaSun } from 'react-icons/fa';
import { Dashboard } from './components/Dashboard';
import { ApplicationList } from './components/ApplicationList';
import { useTheme } from './contexts/ThemeContext';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'applications'>('dashboard');
  const [initialFilter, setInitialFilter] = useState<{ type: string; value: string; timestamp?: number } | null>(null);
  const { isDark, toggleTheme } = useTheme();

  const handleDashboardClick = (filterType: string, filterValue: string) => {
    // Add timestamp to force React to detect this as a new object
    setInitialFilter({ type: filterType, value: filterValue, timestamp: Date.now() });
    setActiveTab('applications');
  };

  return (
    <div className={`min-h-screen ${isDark ? 'dark bg-gray-900' : 'bg-gray-100'}`}>
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold">Job Application Manager</h1>
              <p className="text-blue-100 mt-1">Track your job hunting journey</p>
            </div>
            <button
              onClick={toggleTheme}
              className="p-3 bg-blue-700 hover:bg-blue-600 rounded-full transition-colors"
              title={`Switch to ${isDark ? 'Light' : 'Dark'} Mode`}
            >
              {isDark ? <FaSun className="text-yellow-300" /> : <FaMoon />}
            </button>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white dark:bg-gray-800 shadow-md">
        <div className="container mx-auto px-4">
          <div className="flex gap-4">
            <button
              onClick={() => {
                setActiveTab('dashboard');
                setInitialFilter(null);
              }}
              className={`flex items-center gap-2 px-6 py-4 border-b-2 transition-colors ${
                activeTab === 'dashboard'
                  ? 'border-blue-600 text-blue-600 dark:text-blue-400 font-semibold'
                  : 'border-transparent text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400'
              }`}
            >
              <FaChartBar />
              Dashboard
            </button>
            <button
              onClick={() => {
                setActiveTab('applications');
                setInitialFilter(null);
              }}
              className={`flex items-center gap-2 px-6 py-4 border-b-2 transition-colors ${
                activeTab === 'applications'
                  ? 'border-blue-600 text-blue-600 dark:text-blue-400 font-semibold'
                  : 'border-transparent text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400'
              }`}
            >
              <FaBriefcase />
              Applications
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {activeTab === 'dashboard' ? (
          <Dashboard onCardClick={handleDashboardClick} />
        ) : (
          <ApplicationList initialFilter={initialFilter} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12">
        <div className="container mx-auto px-4 py-6 text-center">
          <p className="text-sm">
            Job Application Manager © 2025
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

