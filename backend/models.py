from typing import List, Optional
from pydantic import BaseModel

# Auth Schemas
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: str
    name: str
    email: str

class AuthResponse(BaseModel):
    user: User
    token: str

# Document Schemas
class Chunk(BaseModel):
    id: int
    source: str
    page: Optional[int] = 1
    tokenCount: Optional[int] = 0
    text: str

class DocumentMetadata(BaseModel):
    id: str
    name: str
    size: int
    type: str
    uploadedAt: str
    status: str
    chunksCount: int
    pagesCount: int
    extractedChars: int
    chunks: List[Chunk] = []

# Research Query Schemas
class ResearchQueryRequest(BaseModel):
    query: str
    documentIds: Optional[List[str]] = None
    topK: Optional[int] = 5

class Citation(BaseModel):
    citationId: int
    chunkId: int
    source: str
    textExcerpt: str
    page: Optional[int] = 1

class ResearchQueryResponse(BaseModel):
    answer: str
    relevantChunks: List[dict]
    citations: List[Citation]
    latencyMs: int
    grounded: bool

# Telemetry & Inspection Schemas
class RetrievalInspectRequest(BaseModel):
    query: str
    documentIds: Optional[List[str]] = None
    topK: Optional[int] = 5

class ScoredChunkItem(BaseModel):
    chunk: dict
    bm25Score: float
    bm25Rank: int
    faissDistance: float
    faissRank: int
    hybridScore: float
    hybridRank: int
    matchedTokens: List[str]

class RetrievalInspectResponse(BaseModel):
    rawQuery: str
    filteredQueryTokens: List[str]
    removedStopwords: List[str]
    topBm25Indices: List[int]
    topFaissIndices: List[int]
    combinedIndices: List[int]
    scoredChunks: List[ScoredChunkItem]
    totalCandidates: int
    retrievalLatencyMs: int
    bm25LatencyMs: int
    faissLatencyMs: int

class HealthResponse(BaseModel):
    status: str
    engineLoaded: bool
    version: str
    indexedDocuments: int
    totalChunks: int

