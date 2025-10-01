import cv2
import base64
import os
import openai

PROMPT = """These are sequential frames from a video.
            Based on this sequence, can you tell me what the people in the video are doing? Did you notice any actions taken by the people in the video?"""

client = openai.OpenAI(
    base_url='http://localhost:8081/v1',
    api_key='ramalama'
)

def analyze_video(video_path, seconds_per_frame=10, model_name='qwen2.5vl:3b'):
    """
    Analyzes a video by extracting frames, sending them to a VLM via ramalama,
    and returning a summary.

    Args:
        video_path (str): The path to the .mp4 video file.
        seconds_per_frame (int): How often to capture a frame from the video.
        model_name (str): The name of the ramalama model to use.

    Returns:
        str: The analysis of the video provided by the model.
    """
    if not os.path.exists(video_path):
        return "Error: Video file not found."

    # Frame Extraction using OpenCV
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * seconds_per_frame)
    
    base64_frames = []
    frame_count = 0
    
    print(f"Extracting frames from '{video_path}' every {seconds_per_frame} seconds...")

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # Capture frame at the specified interval
        if frame_count % frame_interval == 0:
            _, buffer = cv2.imencode(".jpg", frame)
            base64_frame = base64.b64encode(buffer).decode("utf-8")
            base64_frames.append(base64_frame)
        
        frame_count += 1
        
    video.release()
    
    if not base64_frames:
        return "Error: Could not extract any frames from the video."

    print(f"Successfully extracted {len(base64_frames)} frames.")
    print("Sending frames to the VLM for analysis...")
    
    prompt_messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        PROMPT
                    ),
                },
            ],
        }
    ]

    # Add each frame as an image part of the message
    for frame in base64_frames:
        prompt_messages[0]["content"].append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{frame}"},
            }
        )
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=prompt_messages,
            max_tokens=2048, # Adjust as needed
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while communicating with the VLM: {e}"

if __name__ == "__main__":
    video_to_analyze = "classroom.mp4" 
    
    # Analyze one frame every 7 seconds
    analysis = analyze_video(video_to_analyze, seconds_per_frame=7) 
    
    print("\n" + "="*20)
    print("Video Analysis Summary")
    print("="*20)
    print(analysis)
