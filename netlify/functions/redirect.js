let fetch;

exports.handler = async function(event, context) {
  if (!fetch) {
    fetch = (await import('node-fetch')).default;
  }

  const response = await fetch('https://www.scottatron.com/.well-known/build.json');
  const { version } = await response.json();

  const url = `https://github.com/scottatron/scottatron.com/releases/download/${version}/Scott-Arthur-CV-${version}.pdf`

  return {
    statusCode: 302,
    headers: {
      Location: url,
      'Cache-Control': 'no-cache' // Ensure that the function is always called
    }
  };
}
