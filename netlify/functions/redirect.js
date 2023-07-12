exports.handler = async function(event, context) {
  const url = process.env.PDF_URL;

  return {
    statusCode: 302,
    headers: {
      Location: url,
      'Cache-Control': 'no-cache' // Ensure that the function is always called
    }
  };
}
