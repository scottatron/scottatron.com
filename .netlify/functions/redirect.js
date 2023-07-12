const fs = require('fs');
const path = require('path');

exports.handler = async function(event, context) {
  const data = fs.readFileSync(path.join(__dirname, '../public/pdf-url.json'), 'utf8');
  const { url } = JSON.parse(data);

  return {
    statusCode: 302,
    headers: {
      Location: url,
      'Cache-Control': 'no-cache' // Ensure that the function is always called
    }
  };
}
