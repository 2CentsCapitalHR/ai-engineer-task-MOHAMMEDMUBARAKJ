import unittest
import os
from doc_processing import setup_vector_store, augment_analysis

class TestRAG(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a test file with sample ADGM regulations."""
        cls.test_file = "data/adgm_regulations.txt"
        os.makedirs(os.path.dirname(cls.test_file), exist_ok=True)
        
        # Create a sample ADGM regulations text file
        with open(cls.test_file, 'w') as f:
            f.write("Article 1: Annual Returns\n"
                     "Every company must file annual returns with the ADGM.\n"
                     "Article 2: Financial Statements\n"
                     "Companies must prepare financial statements in accordance with the law.")

    def setUp(self):
        """Set up the vector store and QA chain for each test."""
        self.vector_store = setup_vector_store([self.test_file])
        self.qa_chain = augment_analysis(self.vector_store)

    def test_rag_query(self):
        """Test querying the RAG system for Article 1."""
        response = self.qa_chain({"query": "What is Article 1 about?"})
        self.assertIn("annual returns", response["result"].lower())

    def test_rag_query_article_2(self):
        """Test querying the RAG system for Article 2."""
        response = self.qa_chain({"query": "What is Article 2 about?"})
        self.assertIn("financial statements", response["result"].lower())

    @classmethod
    def tearDownClass(cls):
        """Clean up the test file after tests are done."""
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

if __name__ == "__main__":
    unittest.main()
