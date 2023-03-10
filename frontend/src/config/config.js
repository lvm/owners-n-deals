let config;

if (process.env.NODE_ENV === 'production') {
  config = require('./config.prod').default;
} else {
  config = require('./config.dev').default;
}

export default config;