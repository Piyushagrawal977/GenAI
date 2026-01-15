$duration = 5
$mic = "Microphone Array (AMD Audio Device)"
$output = "D:\genai\voice_agent\input.wav"

ffmpeg -y -f dshow -i audio="$mic" -t $duration "$output"
