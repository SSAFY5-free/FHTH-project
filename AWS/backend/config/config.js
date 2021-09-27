module.exports = {
  "development": {
    "database": {
      "url": "mongodb://fhth-mongo/FHTH_dev",
      "options": {
        "useNewUrlParser": true
      }
    }
  },
  "test": {
    "database": {
      "url": "mongodb://fhth-mongo/FHTH_test",
      "options": {
        "useNewUrlParser": true
      }
    }
  },
  "production": {
    "database": {
      "protocol": "mongodb",
      "username": "root",
      "password": "qjawls0501",
      "name": "FHTH_production",
      "host": "fhth-mongo",
      "port": "27017",
      "options": {
        "useNewUrlParser": true
      }
    }
  }
}
