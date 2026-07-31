import whisper
import os

def create_captions(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The media file at {file_path} does not exist.")


    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    print(f"Processing file: {file_path}...")
    result = model.transcribe(file_path)
    
    captions = []
    
    for segment in result['segments']:
        captions.append({
            'id': segment['id'],
            'start': round(segment['start'], 2),
            'end': round(segment['end'], 2),    
            'text': segment['text'].strip()
        })
        
    return captions
