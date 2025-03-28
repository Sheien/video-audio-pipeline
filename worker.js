// Cloudflare Worker: Receives video URL and forwards to yt-dlp microservice
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  if (request.method !== 'POST') {
    return new Response('Only POST allowed', { status: 405 })
  }
  const body = await request.json()
  const { url } = body
  if (!url) return new Response('Missing video URL', { status: 400 })

  const ytDlpEndpoint = 'https://your-ytdlp-service.fly.dev/download'
  const result = await fetch(ytDlpEndpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  })
  return result
}