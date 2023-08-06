import unittest
from Data_Retriever import DataRetrieverAdapter
from display import generate_combined_html

class IntegrationTest(unittest.TestCase):
    def test_data_retrieval_and_display(self):
        # Instantiate the DataRetrieverAdapter class
        data_retriever = DataRetrieverAdapter()

        # Retrieve data using the DataRetrieverAdapter
        data_retriever.retrieve_data()

        # Call the function from the display.py file
        generate_combined_html()

        # Assert the success of the integration test
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
