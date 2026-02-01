import React, { useState, useEffect, useRef } from 'react';
import { Play, Plus, ShieldAlert, MapPin, ArrowRight, Activity, BarChart3 } from 'lucide-react';

// --- SUB-COMPONENT: INCIDENT CARD ---
const IncidentCard = ({ title, time, description, color }) => (
  <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm mb-4 hover:shadow-md transition-shadow font-sans">
    <div className="flex gap-4 items-start">
      <div className={`w-12 h-12 rounded-xl shrink-0 ${color} flex items-center justify-center`}>
        <ShieldAlert className="text-white/80" size={20} />
      </div>
      <div className="flex-1">
        <div className="flex justify-between items-start">
          <h4 className="font-bold text-lg leading-tight">{title}</h4>
          <Plus size={16} className="text-gray-300" />
        </div>
        <div className="flex items-center gap-1 text-[10px] text-gray-400 font-bold uppercase mt-1 tracking-wider">
          <MapPin size={10} /> {time} @ Location
        </div>
        <p className="text-sm text-gray-600 mt-2 leading-relaxed">{description}</p>
      </div>
    </div>
  </div>
);

// --- PAGE 1: HOME PAGE ---
const HomePage = ({ onStart }) => (
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mt-12 animate-in fade-in duration-700 font-sans">
    <div>
      <h1 className="text-7xl font-black italic leading-[1.1] mb-6 tracking-tighter">
        CrimeCatcher.
      </h1>
      <p className="text-xl text-gray-500 max-w-md mb-10">
        A smarter way to monitor crime in real time, for a safer tomorrow.
      </p>
      <button 
        onClick={onStart}
        className="bg-black text-white px-10 py-4 rounded-xl font-bold flex items-center gap-3 hover:scale-105 transition-transform active:scale-95 shadow-lg shadow-black/10"
      >
        Get Started <ArrowRight size={20} />
      </button>
    </div>

    <div className="relative">
      <div className="bg-gray-50 rounded-[3rem] border border-gray-200 aspect-square shadow-2xl overflow-hidden flex flex-col">
        <div className="bg-white border-b border-gray-200 p-5 flex gap-2">
          <div className="w-3 h-3 bg-red-400 rounded-full" />
          <div className="w-3 h-3 bg-yellow-400 rounded-full" />
          <div className="w-3 h-3 bg-green-400 rounded-full" />
        </div>
        <div className="flex-1 grid grid-cols-3 gap-4 p-10 opacity-20">
          {[...Array(9)].map((_, i) => (
            <div key={i} className="bg-gray-400 rounded-2xl" />
          ))}
        </div>
      </div>
    </div>
  </div>
);

// --- PAGE 2: DASHBOARD PAGE ---
const DashboardPage = () => {
  const [incidents, setIncidents] = useState([]);
  const videoRef = useRef(null);

  useEffect(() => {
    // 1. Function to Fetch data from Flask server
    const fetchIncidents = () => {
      fetch('http://127.0.0.1:5001/api/incidents')
        .then(res => res.json())
        .then(data => setIncidents(data))
        .catch(err => console.error("Is the Python server running?", err));
    };

    // Initial fetch
    fetchIncidents();

    // Set up polling (check for new AI detections every 3 seconds)
    const interval = setInterval(fetchIncidents, 3000);

    // 2. Setup Webcam Stream
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch((err) => {
          console.error("Webcam access error:", err);
        });
    }

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-12 gap-10 animate-in slide-in-from-bottom-4 duration-700 font-sans">
      {/* Left Column: Video & Stats */}
      <div className="col-span-12 lg:col-span-8">
        <header className="mb-8">
          <h1 className="text-5xl font-black italic mb-2 tracking-tighter">Live Camera.</h1>
          <p className="text-gray-400 font-semibold">Footage from real time.</p>
        </header>

        {/* Video Box with Webcam Stream */}
        <div className="relative aspect-video bg-black rounded-[2.5rem] shadow-inner mb-10 overflow-hidden flex items-center justify-center border border-gray-100">
          <video 
            ref={videoRef} 
            autoPlay 
            playsInline 
            muted
            className="w-full h-full object-cover scale-x-[-1]" 
          />
          <div className="absolute top-6 left-6 flex items-center gap-2 bg-black/50 backdrop-blur-md px-3 py-1.5 rounded-full border border-white/10">
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
            <span className="text-white text-[10px] font-bold uppercase tracking-wider">Live Feed</span>
          </div>
        </div>

        {/* Bottom Analysis Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="border border-gray-100 rounded-4xl p-8 min-h-45 bg-white">
            <div className="flex items-center gap-2 mb-2">
              <BarChart3 size={18} className="text-gray-400" />
              <h3 className="font-bold">Crime Type Analysis</h3>
            </div>
            <p className="text-xs text-gray-400 leading-relaxed font-medium">Real-time breakdown of detected behaviors.</p>
          </div>
          <div className="border border-gray-100 rounded-4xl p-8 min-h-45 bg-white">
            <div className="flex items-center gap-2 mb-2">
              <Activity size={18} className="text-gray-400" />
              <h3 className="font-bold">Confidence For Crime</h3>
            </div>
            <p className="text-xs text-gray-400 leading-relaxed font-medium">AI model certainty for the current detection.</p>
          </div>
        </div>
      </div>

      {/* Right Column: Sidebar */}
      <div className="col-span-12 lg:col-span-4 bg-gray-50/50 border border-gray-100 rounded-[2.5rem] p-8 flex flex-col h-[calc(100vh-160px)] self-start">
        <h2 className="text-3xl font-black italic mb-1 tracking-tighter">
          Incident <span className="text-gray-400">Dashboard.</span>
        </h2>
        <p className="text-[10px] text-gray-400 uppercase font-bold mb-8 tracking-widest">Real-Time Statistics</p>
        
        <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-2">
          {incidents.length > 0 ? (
            incidents.map((incident) => (
              <IncidentCard 
                key={incident.id}
                title={incident.title} 
                time={incident.time} 
                description={incident.description}
                color={incident.color}
              />
            ))
          ) : (
            <div className="text-center py-20">
              <p className="text-gray-300 text-sm italic font-medium">Waiting for system alerts...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// --- MAIN APP COMPONENT ---
export default function App() {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <div className="min-h-screen bg-white text-slate-900 p-8 lg:p-12 selection:bg-black selection:text-white font-sans">
      {/* NAVBAR */}
      <nav className="flex justify-between items-center mb-12">
        <div 
          className="flex items-center gap-2 cursor-pointer hover:opacity-70 transition-opacity"
          onClick={() => setCurrentPage('home')}
        >
          <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
             <div className="w-4 h-4 bg-white rounded-sm rotate-45" />
          </div>
          <span className="font-black text-2xl tracking-tighter italic">CrimeCatcher.</span>
        </div>
        <div className="hidden md:flex gap-10 text-[13px] font-bold uppercase tracking-tight">
          <button 
            onClick={() => setCurrentPage('dashboard')} 
            className={`transition-all ${currentPage === 'dashboard' ? 'text-black border-b-2 border-black' : 'text-gray-300 hover:text-black'}`}
          >
            Real-Time Analysis
          </button>
          <button className="text-gray-300 hover:text-black transition-colors">Upload</button>
          <button className="text-gray-300 hover:text-black transition-colors">Statistics</button>
        </div>
      </nav>

      {/* CONTENT SWITCHER */}
      {currentPage === 'home' ? (
        <HomePage onStart={() => setCurrentPage('dashboard')} />
      ) : (
        <DashboardPage />
      )}
    </div>
  );
}