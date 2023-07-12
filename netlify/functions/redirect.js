const fs = require('fs')
const path = require('path')

exports.handler = async function(event, context) {
  const buildInfo = fs.readFileSync(path.join(__dirname, '../public/.well-known/build.json'), 'utf-8')
  const {version} = JSON.parse(buildInfo)
  const url = `https://github.com/scottatron/scottatron.com/releases/download/${version}/Scott-Arthur-CV-${version}.pdf`

  return {
    statusCode: 302,
    headers: {
      Location: url,
      'Cache-Control': 'no-cache' // Ensure that the function is always called
    }
  };
}
