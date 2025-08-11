import unittest
import os
from docx import Document
from doc_processing import process_documents

class TestDocumentProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create test documents before running tests"""
        cls.test_dir = "test_documents"
        os.makedirs(cls.test_dir, exist_ok=True)
        
        # Create sample test documents
        cls.create_sample_doc("Articles_of_Association.docx", 
                            ["ARTICLES OF ASSOCIATION",
                             "1. Name: Example Company Ltd.",
                             "2. Jurisdiction: ADGM Courts"])
        
        cls.create_sample_doc("Missing_Jurisdiction.docx",
                            ["MEMORANDUM OF ASSOCIATION",
                             "1. Name: Test Company",
                             "2. No jurisdiction specified"])

    @classmethod
    def create_sample_doc(cls, filename, content):
        """Helper to create test .docx files"""
        doc = Document()
        for line in content:
            doc.add_paragraph(line)
        doc.save(os.path.join(cls.test_dir, filename))

    def test_doc_parsing_success(self):
        """Test successful parsing of valid document"""
        test_file = os.path.join(self.test_dir, "Articles_of_Association.docx")
        with open(test_file, 'rb') as f:
            result = process_documents([f])
            self.assertTrue(result["complete"])
            self.assertEqual(result["jurisdiction_specified"], True)

    def test_missing_jurisdiction(self):
        """Test detection of missing jurisdiction"""
        test_file = os.path.join(self.test_dir, "Missing_Jurisdiction.docx")
        with open(test_file, 'rb') as f:
            result = process_documents([f])
            self.assertIn("High", result["issues"][0]["severity"])
            self.assertEqual(result["jurisdiction_specified"], False)

    def test_checklist_verification(self):
        """Test checklist completeness verification"""
        # Test with all required documents
        test_files = [
            open(os.path.join(self.test_dir, "Articles_of_Association.docx"), 'rb')
        ]
        result = process_documents(test_files)
        self.assertTrue(result["checklist_complete"])
        
        # Close files
        for f in test_files:
            f.close()

if __name__ == "__main__":
    unittest.main()
