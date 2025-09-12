from moviepy import VideoFileClip

# Define the input video file and output audio file
video_path = "Video.mov"
audio_path = "audio.mp3"

# Load the video clip
video_clip = VideoFileClip(video_path)

# Extract the audio from the video clip
audio_clip = video_clip.audio

# Write the audio to a separate file
audio_clip.write_audiofile(audio_path)

# Close the video and audio clips
audio_clip.close()
video_clip.close()