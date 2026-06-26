import os
import math
import subprocess

def format_time(seconds):

    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def generate_srt(captions, srt_path):
    """
    Takes the Whisper captions list and writes them into a valid .srt file.
    """
    with open(srt_path, 'w', encoding='utf-8') as f:
        for i, cap in enumerate(captions, start=1):
            start_time = format_time(cap['start'])
            end_time = format_time(cap['end'])
            text = cap['text']
            

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def attach_captions_to_video(input_path, captions, user_id):

    output_dir = os.path.join("outputs", str(user_id))
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.basename(input_path)
    file_name, ext = os.path.splitext(base_name)

    srt_path = os.path.join(output_dir, f"{file_name}.srt")
    output_path = os.path.join(output_dir, f"{file_name}_captioned{ext}")
    

    generate_srt(captions, srt_path)
    

    safe_srt_path = os.path.abspath(srt_path).replace('\\', '/').replace(':', '\\:')

    command = [
        'ffmpeg',
        '-y',                
        '-i', input_path,    
        '-vf', f"subtitles='{safe_srt_path}'", 
        '-c:a', 'copy',       
        output_path      
    ]
    
    try:
        # Run the command and wait for it to finish
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Success! Captioned video saved to: {output_path}")
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg Error: {e.stderr.decode()}")
        raise Exception("Failed to attach captions to the video.")