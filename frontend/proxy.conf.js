const PROXY_CONFIG = [
  {
    context: [
      "/api",
      "/developers",
    ],
    target: "http://localhost:8000",
    secure: false
  }
]

module.exports = PROXY_CONFIG;
