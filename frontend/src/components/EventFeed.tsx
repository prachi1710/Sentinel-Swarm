'use client';
import { useEffect, useState } from 'react';
import { AlertTriangle, ShieldCheck } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function EventFeed({ onNewEvent }: { onNewEvent: () => void }) {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/events');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      data.id = Date.now().toString() + Math.random().toString();
      setEvents((prev) => [data, ...prev].slice(0, 50));
      onNewEvent(); // Trigger graph refresh
    };

    return () => ws.close();
  }, [onNewEvent]);

  return (
    <div className="h-full overflow-y-auto space-y-3 p-2">
      {events.length === 0 && (
        <div className="text-gray-500 text-center py-4">No events yet. Waiting for simulation...</div>
      )}
      <AnimatePresence>
        {events.map((evt) => {
          const isThreat = evt.data.threat_detected;
          return (
            <motion.div 
              key={evt.id}
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.3 }}
              className={`p-3 rounded-lg border ${isThreat ? 'bg-red-500/10 border-red-500/30 text-red-100 shadow-[0_0_15px_rgba(239,68,68,0.2)]' : 'bg-green-500/10 border-green-500/30 text-green-100'} flex items-start gap-3`}
            >
              {isThreat ? <AlertTriangle className="text-red-400 mt-1 flex-shrink-0" size={20} /> : <ShieldCheck className="text-green-400 mt-1 flex-shrink-0" size={20} />}
              <div>
                <p className="font-semibold">{isThreat ? 'Threat Detected!' : 'Safe Interaction'}</p>
                {isThreat && <p className="text-sm opacity-80 mt-1">Type: {evt.data.threat_details?.threat_type}</p>}
                <p className="text-sm opacity-70 mt-1 break-all">Response: {evt.data.response}</p>
              </div>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
