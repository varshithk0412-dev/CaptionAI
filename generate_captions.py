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

if __name__ == "__main__":
    test_file = "user_uploads/1/test_video.mp4" 
    
    if os.path.exists(test_file):
        try:
            output = create_captions(test_file)
            print("\n--- Generation Successful! ---")
            for cap in output[:3]: # Show first 3 captions
                print(f"[{cap['start']}s -> {cap['end']}s]: {cap['text']}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"To test this script, place a file at: {test_file}")