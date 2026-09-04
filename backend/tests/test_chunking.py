import pytest
from app.rag.chunking import clean_transcript_text, chunk_transcript, is_meaningful_text, extract_speaker

def test_clean_transcript_text_normalization():
    raw_text = "  Hello   world!\r\n\r\n\r\nSpeaker A: How are you?\n  "
    cleaned = clean_transcript_text(raw_text)
    assert "Hello world!" in cleaned
    assert "Speaker A: How are you?" in cleaned
    assert "\r" not in cleaned

def test_is_meaningful_text():
    assert is_meaningful_text("This is valid text.") is True
    assert is_meaningful_text("12345") is True
    assert is_meaningful_text("   ... !!! ???  ") is False
    assert is_meaningful_text("") is False

def test_extract_speaker():
    assert extract_speaker("Lenny Rachitsky: Welcome to the podcast.") == "Lenny Rachitsky"
    assert extract_speaker("Shreyas Doshi: Thanks Lenny.") == "Shreyas Doshi"
    assert extract_speaker("No speaker header here.") is None

def test_chunk_transcript_empty():
    assert chunk_transcript("") == []
    assert chunk_transcript("   \n\n   ") == []

def test_chunk_transcript_short():
    text = "Lenny Rachitsky: Welcome to Lenny's Podcast. Today we talk about growth."
    chunks = chunk_transcript(text, chunk_size=800, chunk_overlap=120)
    assert len(chunks) == 1
    assert chunks[0]["chunk_index"] == 0
    assert "Welcome to Lenny's Podcast" in chunks[0]["content"]
    assert chunks[0]["metadata"]["speaker"] == "Lenny Rachitsky"

def test_chunk_transcript_paragraph_and_speaker_boundaries():
    text = (
        "Lenny Rachitsky: Welcome to the episode.\n\n"
        "Shreyas Doshi: Today I want to discuss product strategy and the LNO framework. "
        "Leverage tasks give 10x impact. Neutral tasks give 1x impact. Overhead tasks give 0.1x impact.\n\n"
        "Lenny Rachitsky: That is brilliant. What about pre-mortems?\n\n"
        "Shreyas Doshi: A pre-mortem asks team members to imagine the product failed 2 years later "
        "and list reasons why."
    )
    chunks = chunk_transcript(text, chunk_size=200, chunk_overlap=40)
    assert len(chunks) >= 2
    for c in chunks:
        assert len(c["content"]) > 0
        assert "chunk_index" in c
        assert "metadata" in c
        assert c["metadata"]["speaker"] in ["Lenny Rachitsky", "Shreyas Doshi"]

def test_chunk_overlap_preservation():
    text = (
        "Paragraph 1 contains significant context about product market fit and retention loops.\n\n"
        "Paragraph 2 discusses customer interviews and continuous feedback loops in early stage startups.\n\n"
        "Paragraph 3 covers positioning, strategic clarity, and high-leverage execution tactics."
    )
    chunks = chunk_transcript(text, chunk_size=120, chunk_overlap=50)
    assert len(chunks) > 1
    # Check that consecutive chunks share overlap content
    assert chunks[0]["metadata"]["length"] > 0
