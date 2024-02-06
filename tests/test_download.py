import pytest
from assignment0.assignment0 import fetchincidents

def test_fetchincidents():
    # Mock a sample URL for testing
    url = "https://example.com/incidents.pdf"
    incident_data = fetchincidents(url)

    assert incident_data is not None
    # Add more assertions based on your requirements
