module.exports = {
  apps: [{
  name: 'app',
  script: './index.js',
  instances: 0,
  exec_mode: "cluster"
  }],
	deploy: {
		production: {
			user: "bure5kzam",
			host: ["127.0.01"],
			ref: "origin/AWS",
			repo: "https://github.com/SSAFY5-free/FHTH_free.git",
			path: "/var/www/repository",
			"post-deploy": "npm install; grunt dist"
		}
	}
}
