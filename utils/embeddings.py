import os
import json
import pickle
from typing import List, Dict, Any, Optional
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RAGEmbeddings:
    def __init__(self, index_path: str = "data/faiss_index", metadata_path: str = "data/metadata.json"):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.dimension = 1536  # OpenAI text-embedding-ada-002 dimension
        self.index = None
        self.metadata = []
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing index or create a new one"""
        try:
            if os.path.exists(self.index_path):
                self.index = faiss.read_index(self.index_path)
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                st.success(f"Loaded existing index with {len(self.metadata)} documents")
            else:
                self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
                self.metadata = []
                st.info("Created new FAISS index")
        except Exception as e:
            st.error(f"Error loading index: {e}")
            self.index = faiss.IndexFlatIP(self.dimension)
            self.metadata = []
    
    def _save_index(self):
        """Save the index and metadata"""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text using OpenAI"""
        try:
            response = client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            st.error(f"Error getting embedding: {e}")
            return []
    
    def add_document(self, text: str, metadata: Dict[str, Any]):
        """Add a document to the index"""
        embedding = self.get_embedding(text)
        if embedding:
            # Normalize the embedding
            embedding = np.array(embedding).reshape(1, -1)
            embedding = embedding / np.linalg.norm(embedding)
            
            self.index.add(embedding.astype('float32'))
            self.metadata.append(metadata)
            self._save_index()
            st.success("Document added to index")
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
        
        # Normalize query embedding
        query_embedding = np.array(query_embedding).reshape(1, -1)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['score'] = float(score)
                result['rank'] = i + 1
                results.append(result)
        
        return results
    
    def get_document_count(self) -> int:
        """Get the number of documents in the index"""
        return len(self.metadata)

# Initialize global RAG instance
@st.cache_resource
def get_rag_instance():
    return RAGEmbeddings()

# Sample data for initialization
SAMPLE_JOB_DESCRIPTIONS = [
    {
        "text": "Data Analyst position requiring SQL, Python, Tableau, and statistical analysis skills. Experience with data visualization and business intelligence tools preferred.",
        "metadata": {
            "type": "job_description",
            "title": "Data Analyst",
            "company": "Tech Corp",
            "skills": ["SQL", "Python", "Tableau", "Statistical Analysis", "Data Visualization"],
            "experience_level": "Mid-level"
        }
    },
    {
        "text": "Machine Learning Engineer role focusing on developing and deploying ML models. Requirements include Python, TensorFlow/PyTorch, AWS, and experience with production ML systems.",
        "metadata": {
            "type": "job_description",
            "title": "Machine Learning Engineer",
            "company": "AI Startup",
            "skills": ["Python", "TensorFlow", "PyTorch", "AWS", "MLOps", "Docker"],
            "experience_level": "Senior"
        }
    },
    {
        "text": "Software Engineer position for backend development. Skills needed: Java, Spring Boot, PostgreSQL, Docker, and microservices architecture.",
        "metadata": {
            "type": "job_description",
            "title": "Backend Software Engineer",
            "company": "FinTech Inc",
            "skills": ["Java", "Spring Boot", "PostgreSQL", "Docker", "Microservices"],
            "experience_level": "Mid-level"
        }
    }
]

SAMPLE_RESUME_EXAMPLES = [
    {
        "text": "Experienced data analyst with 3+ years in SQL, Python, and Tableau. Led data-driven projects improving business metrics by 25%. Strong background in statistical analysis and A/B testing.",
        "metadata": {
            "type": "resume_example",
            "title": "Data Analyst Resume",
            "experience_years": 3,
            "skills": ["SQL", "Python", "Tableau", "Statistical Analysis", "A/B Testing"],
            "success_rate": "High"
        }
    },
    {
        "text": "Senior ML Engineer with expertise in TensorFlow, PyTorch, and cloud deployment. Built production ML pipelines serving 1M+ users. Experience with MLOps, Docker, and AWS services.",
        "metadata": {
            "type": "resume_example",
            "title": "ML Engineer Resume",
            "experience_years": 5,
            "skills": ["TensorFlow", "PyTorch", "AWS", "MLOps", "Docker", "Python"],
            "success_rate": "High"
        }
    }
]

def initialize_sample_data():
    """Initialize the RAG system with sample data"""
    rag = get_rag_instance()
    
    if rag.get_document_count() == 0:
        st.info("Initializing RAG system with sample data...")
        
        # Add sample job descriptions
        for job in SAMPLE_JOB_DESCRIPTIONS:
            rag.add_document(job["text"], job["metadata"])
        
        # Add sample resume examples
        for resume in SAMPLE_RESUME_EXAMPLES:
            rag.add_document(resume["text"], resume["metadata"])
        
        st.success("RAG system initialized with sample data!")

