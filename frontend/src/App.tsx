import React from 'react';
import { useApp } from './context/AppContext';
import { Header } from './components/layout/Header';
import { Sidebar } from './components/layout/Sidebar';
import { DisclaimerModal } from './components/layout/DisclaimerModal';

// Pages
import { DashboardPage } from './pages/DashboardPage';
import { RiskMapPage } from './pages/RiskMapPage';
import { AlertsPage } from './pages/AlertsPage';
import { AlertDetailsPage } from './pages/AlertDetailsPage';
import { SatelliteTimelinePage } from './pages/SatelliteTimelinePage';
import { MiningLeasesPage } from './pages/MiningLeasesPage';
import { ChangeDetectionPage } from './pages/ChangeDetectionPage';
import { AIModelsPage } from './pages/AIModelsPage';
import { FieldVerificationPage } from './pages/FieldVerificationPage';
import { DataSourcesPage } from './pages/DataSourcesPage';
import { SystemArchitecturePage } from './pages/SystemArchitecturePage';
import { SettingsPage } from './pages/SettingsPage';
import { ReportViewPage } from './pages/ReportViewPage';

export const AppContent: React.FC = () => {
  const { currentPage } = useApp();

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <DashboardPage />;
      case 'risk-map':
        return <RiskMapPage />;
      case 'alerts':
        return <AlertsPage />;
      case 'alert-details':
        return <AlertDetailsPage />;
      case 'satellite-analysis':
        return <SatelliteTimelinePage />;
      case 'mining-leases':
        return <MiningLeasesPage />;
      case 'change-detection':
        return <ChangeDetectionPage />;
      case 'ai-models':
        return <AIModelsPage />;
      case 'field-verification':
        return <FieldVerificationPage />;
      case 'reports':
        return <ReportViewPage />;
      case 'data-sources':
        return <DataSourcesPage />;
      case 'system-architecture':
        return <SystemArchitecturePage />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans text-slate-900">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-4 md:p-6 custom-scrollbar">
          {renderCurrentPage()}
        </main>
      </div>
      <DisclaimerModal />
    </div>
  );
};

export const App: React.FC = () => {
  return <AppContent />;
};

export default App;
