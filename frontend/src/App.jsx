import { useEffect, useState } from "react"
import DocumentUpload from "./components/DocumentUpload"
import ChatPanel from "./components/ChatPanel"

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

export default function App() {
    const [docId, setDocId] = useState(null)
    const [backendStatus, setBackendStatus] = useState("checking")

    useEffect(() => {
        async function checkHealth() {
            try {
                const res = await fetch(`${API}/health`)
                if (!res.ok) throw new Error("Health check failed")
                setBackendStatus("online")
            } catch {
                setBackendStatus("offline")
            }
        }

        checkHealth()
    }, [])

    return (
        <div
            style={{
                minHeight: "100vh",
                background: "var(--bg)",
                display: "flex",
                flexDirection: "column"
            }}
        >
            <header
                style={{
                    borderBottom: "1px solid var(--border)",
                    padding: "0 40px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    height: "60px",
                    background: "var(--bg)",
                    position: "sticky",
                    top: 0,
                    zIndex: 10
                }}
            >
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <div
                        style={{
                            width: "36px",
                            height: "36px",
                            borderRadius: "8px",
                            background: "#0f1f12",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            overflow: "hidden"
                        }}
                    >
                        <img
                            src="/logo.png"
                            alt="ClinicalQA"
                            style={{ width: "32px", height: "32px", objectFit: "contain" }}
                        />
                    </div>

                    <span
                        style={{
                            fontSize: "15px",
                            fontWeight: "600",
                            letterSpacing: "-0.02em",
                            color: "var(--text)"
                        }}
                    >
                        ClinicalQA
                    </span>

                    <span
                        style={{
                            fontSize: "10px",
                            color: "var(--text-dim)",
                            fontFamily: "'Space Mono', monospace",
                            letterSpacing: "0.1em",
                            textTransform: "uppercase",
                            marginLeft: "4px",
                            paddingTop: "2px"
                        }}
                    >
                        / RAG
                    </span>
                </div>

                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "8px",
                            fontSize: "11px",
                            fontFamily: "'Space Mono', monospace",
                            color:
                                backendStatus === "online"
                                    ? "var(--green)"
                                    : backendStatus === "offline"
                                        ? "#ef4444"
                                        : "var(--text-dim)",
                            background: "var(--bg-card)",
                            border: "1px solid var(--border)",
                            borderRadius: "6px",
                            padding: "5px 12px"
                        }}
                    >
                        <span
                            style={{
                                width: "6px",
                                height: "6px",
                                borderRadius: "50%",
                                background:
                                    backendStatus === "online"
                                        ? "var(--green)"
                                        : backendStatus === "offline"
                                            ? "#ef4444"
                                            : "var(--text-dim)",
                                display: "inline-block",
                                boxShadow:
                                    backendStatus === "online"
                                        ? "0 0 8px var(--green)"
                                        : "none"
                            }}
                        />
                        {backendStatus}
                    </div>

                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "8px",
                            fontSize: "11px",
                            fontFamily: "'Space Mono', monospace",
                            color: docId ? "var(--green)" : "var(--text-dim)",
                            background: "var(--bg-card)",
                            border: "1px solid var(--border)",
                            borderRadius: "6px",
                            padding: "5px 12px",
                            maxWidth: "320px"
                        }}
                        title={docId || "no document"}
                    >
                        <span
                            style={{
                                width: "6px",
                                height: "6px",
                                borderRadius: "50%",
                                background: docId ? "var(--green)" : "var(--text-dim)",
                                display: "inline-block",
                                boxShadow: docId ? "0 0 8px var(--green)" : "none"
                            }}
                        />
                        <span
                            style={{
                                whiteSpace: "nowrap",
                                overflow: "hidden",
                                textOverflow: "ellipsis"
                            }}
                        >
                            {docId || "no document"}
                        </span>
                    </div>
                </div>
            </header>

            <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
                <aside
                    style={{
                        width: "280px",
                        minWidth: "280px",
                        borderRight: "1px solid var(--border)",
                        padding: "28px 20px",
                        display: "flex",
                        flexDirection: "column",
                        gap: "20px",
                        background: "var(--bg)"
                    }}
                >
                    <DocumentUpload onUpload={setDocId} />

                    <div style={{ marginTop: "auto" }}>
                        <div
                            style={{
                                background: "var(--bg-card)",
                                border: "1px solid var(--border)",
                                borderRadius: "10px",
                                padding: "16px",
                                borderLeft: "3px solid var(--green-muted)"
                            }}
                        >
                            <div
                                style={{
                                    fontSize: "10px",
                                    color: "var(--green)",
                                    fontFamily: "'Space Mono', monospace",
                                    letterSpacing: "0.1em",
                                    marginBottom: "10px"
                                }}
                            >
                                // HOW IT WORKS
                            </div>

                            {[
                                "Structured chunking with metadata (custom chunker)",
                                "Embeddings via sentence-transformers (all-MiniLM-L6-v2)",
                                "Vector storage using ChromaDB (persistent)",
                                "Dense retrieval using FAISS similarity search",
                                "Reranking via cross-encoder (ms-marco-MiniLM-L-6-v2)",
                                "LLM inference via Gemini / Anthropic (provider-based)",
                                "Grounded responses with source and page citations"
                                ].map((t, i) => (
                                <div
                                    key={i}
                                    style={{
                                        display: "flex",
                                        gap: "10px",
                                        marginBottom: "8px",
                                        alignItems: "flex-start"
                                    }}
                                >
                                    <span
                                        style={{
                                            color: "var(--green)",
                                            fontSize: "11px",
                                            fontFamily: "'Space Mono', monospace",
                                            minWidth: "16px"
                                        }}
                                    >
                                        {String(i + 1).padStart(2, "0")}
                                    </span>
                                    <span
                                        style={{
                                            fontSize: "12px",
                                            color: "var(--text-muted)",
                                            lineHeight: 1.5
                                        }}
                                    >
                                        {t}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </aside>

                <main
                    style={{
                        flex: 1,
                        padding: "32px 40px",
                        display: "flex",
                        flexDirection: "column",
                        overflow: "hidden"
                    }}
                >
                    <ChatPanel docId={docId} />
                </main>
            </div>
        </div>
    )
}