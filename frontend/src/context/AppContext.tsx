import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserProfile, UserRole, GlobalMiningSite } from '../types';
import { apiClient } from '../api/client';

interface AppContextType {
  selectedRegion: string;
  setSelectedRegion: (region: string) => void;
  currentRole: UserRole;
  setCurrentRole: (role: UserRole) => void;
  user: UserProfile | null;
  disclaimerOpen: boolean;
  setDisclaimerOpen: (open: boolean) => void;
  currentPage: string;
  setCurrentPage: (page: string) => void;
  activeAlertId: string | null;
  navigateToAlert: (alertId: string) => void;
  isRealDataMode: boolean;
  setIsRealDataMode: (mode: boolean) => void;
  selectedGlobalMiningSite: GlobalMiningSite | null;
  setSelectedGlobalMiningSite: (site: GlobalMiningSite | null) => void;
  activeAOI: any;
  setActiveAOI: (aoi: any) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedRegion, setSelectedRegion] = useState<string>('Keonjhar');
  const [currentRole, setCurrentRole] = useState<UserRole>('ADMIN');
  const [user, setUser] = useState<UserProfile | null>(null);
  const [disclaimerOpen, setDisclaimerOpen] = useState<boolean>(false);
  const [currentPage, setCurrentPage] = useState<string>('dashboard');
  const [activeAlertId, setActiveAlertId] = useState<string | null>('MG-2026-00421');
  
  // Real Data Mode vs Demo Mode (Default: Real Data Mode)
  const [isRealDataMode, setIsRealDataMode] = useState<boolean>(true);
  const [selectedGlobalMiningSite, setSelectedGlobalMiningSite] = useState<GlobalMiningSite | null>(null);
  const [activeAOI, setActiveAOI] = useState<any>(null);

  useEffect(() => {
    apiClient.getCurrentUser(currentRole).then(setUser).catch(console.error);
  }, [currentRole]);

  const navigateToAlert = (alertId: string) => {
    setActiveAlertId(alertId);
    setCurrentPage('alert-details');
  };

  return (
    <AppContext.Provider
      value={{
        selectedRegion,
        setSelectedRegion,
        currentRole,
        setCurrentRole,
        user,
        disclaimerOpen,
        setDisclaimerOpen,
        currentPage,
        setCurrentPage,
        activeAlertId,
        navigateToAlert,
        isRealDataMode,
        setIsRealDataMode,
        selectedGlobalMiningSite,
        setSelectedGlobalMiningSite,
        activeAOI,
        setActiveAOI
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
