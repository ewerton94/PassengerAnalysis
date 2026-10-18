import fs from 'fs'

fs.writeFileSync('./.env', `GoogleMapsKey=${process.env.GoogleMapsKey || ''}\n`)
