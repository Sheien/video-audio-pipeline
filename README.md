# Video Audio Pipeline

## Cloudflare Worker
Handles incoming video URLs and calls yt-dlp microservice.

## yt-dlp Service
Extracts audio from YouTube/TikTok videos using yt-dlp.

### Deployment:
1. Deploy `yt-dlp-service` to Fly.io or Render
2. Deploy `cloudflare-worker` with Wrangler
3. Connect it all to Xano
4. Use WeWeb to trigger your flow

You’re now ready to extract, transcribe, and summarize video audio 🚀