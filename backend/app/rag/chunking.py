import re
from typing import List, Dict, Any, Optional

def clean_transcript_text(text: str) -> str:
    """Normalize whitespace and line breaks while preserving paragraph boundaries and speaker turns."""
    if not text:
        return ""
    
    # Standardize line endings
    cleaned = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Replace multiple blank lines with a double newline
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    
    # Normalize inline spaces (replace tabs and multiple spaces with single space)
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in cleaned.split('\n')]
    
    # Rejoin with standard newlines
    cleaned = '\n'.join(lines)
    
    # Ensure double newlines before speaker turns (e.g. "Speaker Name:")
    cleaned = re.sub(r'(\n|^)([A-Z][a-zA-Z\s]{1,30}:)', r'\1\n\2', cleaned)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned).strip()
    
    return cleaned

def is_meaningful_text(text: str) -> bool:
    """Check if chunk text contains meaningful alphanumeric content."""
    if not text or not text.strip():
        return False
    # Must contain at least 5 alphanumeric characters
    alpha_count = len(re.findall(r'[a-zA-Z0-9]', text))
    return alpha_count >= 5

def extract_speaker(text: str) -> Optional[str]:
    """Extract speaker name if text starts with 'Speaker Name:' format."""
    match = re.match(r'^([A-Z][a-zA-Z\s]{1,30}):', text.strip())
    if match:
        return match.group(1).strip()
    return None

def chunk_transcript(
    content: str,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
    default_speaker: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Split transcript text into semantic chunks respecting paragraph and speaker boundaries.
    
    Args:
        content: Cleaned raw transcript text
        chunk_size: Target character size per chunk (default 800)
        chunk_overlap: Target character overlap between consecutive chunks (default 120)
        default_speaker: Default speaker name for transcript if available
        
    Returns:
        List of dicts containing chunk_index, content, start_char, end_char, and metadata
    """
    cleaned_content = clean_transcript_text(content)
    if not cleaned_content:
        return []
    
    # Split text into structural paragraphs / blocks
    blocks = [b.strip() for b in cleaned_content.split('\n\n') if b.strip()]
    if not blocks:
        blocks = [cleaned_content]

    chunks = []
    current_chunk_blocks = []
    current_length = 0
    current_speaker = default_speaker
    chunk_index = 0
    
    start_char_offset = 0

    for block in blocks:
        block_speaker = extract_speaker(block)
        if block_speaker:
            current_speaker = block_speaker
            
        block_len = len(block)
        
        # If adding block exceeds chunk size and we already have content
        if current_length > 0 and (current_length + block_len + 2) > chunk_size:
            chunk_text = "\n\n".join(current_chunk_blocks).strip()
            
            if is_meaningful_text(chunk_text):
                end_offset = start_char_offset + len(chunk_text)
                chunks.append({
                    "chunk_index": chunk_index,
                    "content": chunk_text,
                    "start_char": start_char_offset,
                    "end_char": end_offset,
                    "metadata": {
                        "speaker": current_speaker,
                        "length": len(chunk_text)
                    }
                })
                chunk_index += 1

            # Prepare overlap for next chunk
            overlap_blocks = []
            overlap_length = 0
            for prev_block in reversed(current_chunk_blocks):
                if overlap_length + len(prev_block) + 2 <= chunk_overlap:
                    overlap_blocks.insert(0, prev_block)
                    overlap_length += len(prev_block) + 2
                else:
                    break
            
            current_chunk_blocks = overlap_blocks
            current_length = overlap_length
            start_char_offset = end_offset - overlap_length if end_offset > overlap_length else 0

        current_chunk_blocks.append(block)
        current_length += block_len + 2

    # Add final remaining chunk
    if current_chunk_blocks:
        chunk_text = "\n\n".join(current_chunk_blocks).strip()
        if is_meaningful_text(chunk_text):
            chunks.append({
                "chunk_index": chunk_index,
                "content": chunk_text,
                "start_char": start_char_offset,
                "end_char": start_char_offset + len(chunk_text),
                "metadata": {
                    "speaker": current_speaker,
                    "length": len(chunk_text)
                }
            })

    return chunks
