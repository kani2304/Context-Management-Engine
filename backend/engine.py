import time
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import faiss
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from .config import CONVERSATIONAL_STOPWORDS, EMBEDDING_MODEL_NAME

class HybridRAGEngine:
    """
    Dual-retrieval pipeline combining:
    1. Lexical ranking via BM25Okapi with conversational stopword filtering.
    2. Dense semantic ranking via SentenceTransformers (all-MiniLM-L6-v2) and FAISS IndexFlatL2.
    """
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        print(f"[HybridRAGEngine] Loading embedding model: {model_name}...", flush=True)
        self.embedding_model = SentenceTransformer(model_name)
        self.chunks: List[Dict[str, Any]] = []
        self.bm25: Optional[BM25Okapi] = None
        self.faiss_index: Optional[faiss.IndexFlatL2] = None

    def index_documents(self, chunks: List[Dict[str, Any]]) -> None:
        """Indexes chunks into both BM25 and FAISS indexes."""
        self.chunks = chunks
        if not chunks:
            self.bm25 = None
            self.faiss_index = None
            return

        # 1. Build Lexical BM25 Index
        tokenized_corpus = [chunk["text"].lower().split() for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)

        # 2. Build Dense Vector FAISS Index
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        dimension = embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(embeddings)
        print(f"[HybridRAGEngine] Successfully indexed {len(chunks)} chunks across BM25 and FAISS.", flush=True)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieves top candidates using hybrid union of BM25 and FAISS."""
        if not self.chunks or self.bm25 is None or self.faiss_index is None:
            return []

        # 1. Lexical BM25 Retrieval with query filtering
        raw_tokens = query.lower().split()
        filtered_tokens = [w for w in raw_tokens if w not in CONVERSATIONAL_STOPWORDS]
        bm25_query = filtered_tokens if filtered_tokens else raw_tokens

        bm25_scores = self.bm25.get_scores(bm25_query)
        top_bm25_indices = np.argsort(bm25_scores)[::-1][:top_k]

        # 2. Dense Semantic FAISS Retrieval
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True, show_progress_bar=False)
        _, top_faiss_indices = self.faiss_index.search(query_embedding, top_k)

        # 3. Hybrid Union
        combined_indices = set(top_bm25_indices).union(set(top_faiss_indices[0]))
        return [self.chunks[i] for i in combined_indices if i < len(self.chunks)]

    def inspect(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Provides deep telemetry on query tokens, BM25 scores, FAISS distances, and hybrid ranks."""
        if not self.chunks or self.bm25 is None or self.faiss_index is None:
            return {}

        start_time = time.time()
        raw_tokens = query.lower().split()
        filtered_tokens = [w for w in raw_tokens if w not in CONVERSATIONAL_STOPWORDS]
        removed_stopwords = [w for w in raw_tokens if w in CONVERSATIONAL_STOPWORDS]

        # BM25 timing
        bm25_start = time.time()
        bm25_query = filtered_tokens if filtered_tokens else raw_tokens
        bm25_scores = self.bm25.get_scores(bm25_query)
        top_bm25_indices = [int(i) for i in np.argsort(bm25_scores)[::-1][:top_k]]
        bm25_latency = int((time.time() - bm25_start) * 1000)

        # FAISS timing
        faiss_start = time.time()
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True, show_progress_bar=False)
        distances, top_faiss_indices = self.faiss_index.search(query_embedding, top_k)
        top_faiss_indices = [int(i) for i in top_faiss_indices[0]]
        faiss_latency = int((time.time() - faiss_start) * 1000)

        combined_indices = list(set(top_bm25_indices).union(set(top_faiss_indices)))
        total_latency = int((time.time() - start_time) * 1000)

        scored_chunks = []
        for rank, idx in enumerate(combined_indices):
            if idx >= len(self.chunks):
                continue
            chunk = self.chunks[idx]
            b_score = float(bm25_scores[idx]) if idx < len(bm25_scores) else 0.0
            
            f_dist = 1.0
            if idx in top_faiss_indices:
                pos = top_faiss_indices.index(idx)
                f_dist = float(distances[0][pos])

            scored_chunks.append({
                "chunk": chunk,
                "bm25Score": round(b_score, 2),
                "bm25Rank": top_bm25_indices.index(idx) + 1 if idx in top_bm25_indices else len(top_bm25_indices) + 1,
                "faissDistance": round(f_dist, 3),
                "faissRank": top_faiss_indices.index(idx) + 1 if idx in top_faiss_indices else len(top_faiss_indices) + 1,
                "hybridScore": round((1 / (60 + (rank + 1))), 4),
                "hybridRank": rank + 1,
                "matchedTokens": [t for t in filtered_tokens if t in chunk["text"].lower()],
            })

        return {
            "rawQuery": query,
            "filteredQueryTokens": filtered_tokens,
            "removedStopwords": removed_stopwords,
            "topBm25Indices": top_bm25_indices,
            "topFaissIndices": top_faiss_indices,
            "combinedIndices": combined_indices,
            "scoredChunks": scored_chunks,
            "totalCandidates": len(self.chunks),
            "retrievalLatencyMs": total_latency,
            "bm25LatencyMs": max(1, bm25_latency),
            "faissLatencyMs": max(1, faiss_latency),
        }

