import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Trash2, Plus, TrendingUp, AlertTriangle, ExternalLink, Activity } from 'lucide-react';
import { cn } from '../lib/utils';
import { format } from 'date-fns';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// --- Types ---
interface Ticker {
    id: number;
    symbol: string;
}

interface NewsAlert {
    id: number;
    ticker: string;
    title: string;
    summary: string;
    impact: string;
    link: string;
    image_url?: string;
    created_at: string;
}

// --- API Functions ---
const fetchTickers = async () => (await axios.get<Ticker[]>(`${API_URL}/tickers`)).data;
const addTicker = async (symbol: string) => (await axios.post(`${API_URL}/tickers`, { symbol: symbol.toUpperCase() })).data;
const deleteTicker = async (id: number) => (await axios.delete(`${API_URL}/tickers/${id}`)).data;
// const fetchAlerts = async () => (await axios.get<NewsAlert[]>(`${API_URL}/alerts`)).data;

// --- Components ---

const TickerBadge = ({ ticker, onDelete }: { ticker: Ticker; onDelete: (id: number) => void }) => (
    <motion.div
        layout
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.8 }}
        className="flex items-center gap-2 bg-secondary/50 hover:bg-secondary px-3 py-1.5 rounded-full text-sm font-medium transition-colors border border-white/5"
    >
        <span>{ticker.symbol}</span>
        <button
            onClick={() => onDelete(ticker.id)}
            className="text-muted-foreground hover:text-destructive transition-colors p-0.5"
        >
            <Trash2 className="w-3.5 h-3.5" />
        </button>
    </motion.div>
);

const ImpactBadge = ({ impact }: { impact: string }) => {
    // Extract number if present "5 Positive" -> 5
    const score = parseInt(impact.split(' ')[0]) || 0;
    let color = "bg-gray-500/20 text-gray-400 border-gray-500/20";

    if (score >= 4) color = "bg-red-500/20 text-red-500 border-red-500/20";
    else if (score === 3) color = "bg-yellow-500/20 text-yellow-500 border-yellow-500/20";
    else if (score > 0) color = "bg-green-500/20 text-green-500 border-green-500/20";

    return (
        <span className={cn("px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider border", color)}>
            {impact}
        </span>
    );
};

const NewsCard = ({ alert }: { alert: NewsAlert }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-card hover:bg-card/80 border border-white/5 rounded-xl transition-colors group overflow-hidden flex flex-col"
    >
        {alert.image_url && (
            <div className="w-full h-48 overflow-hidden relative">
                <img
                    src={alert.image_url}
                    alt={alert.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    onError={(e) => (e.currentTarget.style.display = 'none')}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                <div className="absolute bottom-3 left-3">
                    <ImpactBadge impact={alert.impact} />
                </div>
            </div>
        )}

        <div className="p-5 flex-1 flex flex-col">
            <div className="flex justify-between items-start mb-3">
                <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-lg text-primary">{alert.ticker}</span>
                    {!alert.image_url && <ImpactBadge impact={alert.impact} />}
                </div>
                <span className="text-xs text-muted-foreground">
                    {format(new Date(alert.created_at), 'MMM d, h:mm a')}
                </span>
            </div>

            <h3 className="font-semibold text-lg mb-2 leading-snug group-hover:text-blue-400 transition-colors">
                <a href={alert.link} target="_blank" rel="noreferrer" className="flex items-center gap-1">
                    {alert.title}
                </a>
            </h3>
            <p className="text-muted-foreground text-sm mb-4 leading-relaxed line-clamp-2">
                {alert.summary}
            </p>

            <div className="mt-auto pt-4 flex justify-end">
                <a
                    href={alert.link}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 text-xs font-medium text-primary hover:text-primary/80 transition-colors"
                >
                    Read Source <ExternalLink className="w-3 h-3" />
                </a>
            </div>
        </div>
    </motion.div>
);

// --- Components ---

const UserManual = ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => (
    <AnimatePresence>
        {isOpen && (
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
                onClick={onClose}
            >
                <motion.div
                    initial={{ scale: 0.9, y: 20 }}
                    animate={{ scale: 1, y: 0 }}
                    exit={{ scale: 0.9, y: 20 }}
                    className="bg-card border border-white/10 p-8 rounded-2xl max-w-2xl w-full shadow-2xl space-y-6"
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="space-y-2">
                        <h2 className="text-2xl font-bold text-primary">How to Use the Stock News Agent</h2>
                        <p className="text-muted-foreground text-sm">Your 24/7 AI-powered financial market intelligence assistant.</p>
                    </div>

                    <div className="grid gap-6 py-2">
                        <div className="flex gap-4">
                            <div className="bg-primary/20 p-2 rounded-lg h-fit">
                                <Plus className="w-5 h-5 text-primary" />
                            </div>
                            <div>
                                <h3 className="font-semibold mb-1">Step 1: Build Your Watchlist</h3>
                                <p className="text-sm text-muted-foreground">Add stock tickers (e.g., AAPL, TSLA) to the watchlist in the sidebar. The agent will only monitor news for stocks you track.</p>
                            </div>
                        </div>

                        <div className="flex gap-4">
                            <div className="bg-green-500/20 p-2 rounded-lg h-fit">
                                <TrendingUp className="w-5 h-5 text-green-500" />
                            </div>
                            <div>
                                <h3 className="font-semibold mb-1">Step 2: AI Impact Analysis</h3>
                                <p className="text-sm text-muted-foreground">The agent automatically scans RSS feeds every 10 minutes. Llama 3.1 AI reads each article to score its market impact from 1 to 5.</p>
                            </div>
                        </div>

                        <div className="flex gap-4">
                            <div className="bg-blue-500/20 p-2 rounded-lg h-fit">
                                <Activity className="w-5 h-5 text-blue-500" />
                            </div>
                            <div>
                                <h3 className="font-semibold mb-1">Step 3: Act on Intelligence</h3>
                                <p className="text-sm text-muted-foreground">High-impact news (4-5) is highlighted in red. Use the AI summary to quickly grasp the significance without reading the full article.</p>
                            </div>
                        </div>
                    </div>

                    <button
                        onClick={onClose}
                        className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-3 rounded-xl transition-all shadow-lg"
                    >
                        Got it, let's go!
                    </button>
                </motion.div>
            </motion.div>
        )}
    </AnimatePresence>
);

export default function Dashboard() {
    // --- State ---
    const [newTicker, setNewTicker] = useState("");
    const [isManualOpen, setIsManualOpen] = useState(true);

    // --- Queries ---
    const queryClient = useQueryClient();

    const { data: tickers = [] } = useQuery({ queryKey: ['tickers'], queryFn: fetchTickers });

    // Use React Query polling for real-time-like updates
    const { data: alerts = [] } = useQuery({
        queryKey: ['alerts'],
        queryFn: async () => (await axios.get<NewsAlert[]>(`${API_URL}/alerts`)).data,
        refetchInterval: 10000 // Poll every 10s
    });

    // --- Mutations ---
    const addMutation = useMutation({
        mutationFn: addTicker,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tickers'] });
            setNewTicker("");
        },
        onError: (err) => alert("Failed to add ticker. It might already exist.")
    });

    const deleteMutation = useMutation({
        mutationFn: deleteTicker,
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tickers'] })
    });

    const handleAddTicker = (e: React.FormEvent) => {
        e.preventDefault();
        if (newTicker.trim()) addMutation.mutate(newTicker);
    }

    // Stats
    const highImpactCount = alerts.filter(a => (parseInt(a.impact.split(' ')[0]) || 0) >= 4).length;

    return (
        <div className="max-w-7xl mx-auto p-6 space-y-8">
            <UserManual isOpen={isManualOpen} onClose={() => setIsManualOpen(false)} />

            {/* Header */}
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/5">
                <div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent flex items-center gap-3">
                        <Activity className="w-8 h-8 text-blue-400" />
                        Stock News Agent
                    </h1>
                    <div className="flex items-center gap-3 mt-1">
                        <p className="text-muted-foreground">Real-time market intelligence & impact analysis</p>
                        <button
                            onClick={() => setIsManualOpen(true)}
                            className="text-xs text-primary hover:underline font-medium"
                        >
                            Open User Manual
                        </button>
                    </div>
                </div>

                <div className="flex gap-4">
                    <div className="bg-card border border-white/5 px-4 py-2 rounded-lg text-center min-w-[100px]">
                        <div className="text-2xl font-bold">{alerts.length}</div>
                        <div className="text-xs text-muted-foreground uppercase tracking-widest">Alerts</div>
                    </div>
                    <div className="bg-red-500/10 border border-red-500/20 px-4 py-2 rounded-lg text-center min-w-[100px]">
                        <div className="text-2xl font-bold text-red-400">{highImpactCount}</div>
                        <div className="text-xs text-red-400/70 uppercase tracking-widest">High Impact</div>
                    </div>
                </div>
            </header>

            {/* Main Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">

                {/* Sidebar: Ticker Management */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-card border border-white/10 rounded-xl p-5 sticky top-6">
                        <h2 className="font-semibold text-lg mb-4 flex items-center gap-2">
                            <TrendingUp className="w-5 h-5 text-green-400" /> Watchlist
                        </h2>

                        <form onSubmit={handleAddTicker} className="flex gap-2 mb-4">
                            <input
                                value={newTicker}
                                onChange={(e) => setNewTicker(e.target.value)}
                                placeholder="Add Ticker (e.g. NVDA)"
                                className="flex-1 bg-background border border-white/10 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 uppercase"
                            />
                            <button
                                type="submit"
                                disabled={addMutation.isPending}
                                className="bg-primary hover:bg-primary/90 text-primary-foreground p-2 rounded-lg transition-colors"
                            >
                                <Plus className="w-5 h-5" />
                            </button>
                        </form>

                        <div className="flex flex-wrap gap-2">
                            <AnimatePresence>
                                {tickers.map(t => (
                                    <TickerBadge key={t.id} ticker={t} onDelete={deleteMutation.mutate} />
                                ))}
                                {tickers.length === 0 && (
                                    <span className="text-sm text-muted-foreground italic">No tickers added.</span>
                                )}
                            </AnimatePresence>
                        </div>
                    </div>
                </div>

                {/* Main Feed */}
                <div className="lg:col-span-3 space-y-6">
                    <h2 className="font-semibold text-xl flex items-center gap-2">
                        <span className="relative flex h-3 w-3">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
                        </span>
                        Live Market Feed
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {alerts.length === 0 ? (
                            <div className="col-span-full py-20 text-center text-muted-foreground border-2 border-dashed border-white/5 rounded-xl">
                                No alerts generated yet. Add tickers and wait for the agent to fetch news.
                            </div>
                        ) : (
                            alerts.map(alert => (
                                <NewsCard key={alert.id} alert={alert} />
                            ))
                        )}
                    </div>
                </div>

            </div>
        </div>
    );
}
