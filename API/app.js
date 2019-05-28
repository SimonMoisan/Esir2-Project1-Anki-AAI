const express = require('express')
const bodyParser = require('body-parser')
const helmet = require('helmet')
const cors = require('cors')

const answersRouter = require('./routes/answers-v1')
const answersModel = require('./model/answers')
const imagesRouter = require('./routes/images-v1')
const imagesModel = require('./model/images')

const app = express()

// Activation de Helmet
app.use(helmet({noSniff: true}))
app.use(cors())

// On injecte le model dans les routers. Ceci permet de supprimer la dépendance
// directe entre les routers et le modele
app.use(bodyParser.json({limit: '200mb'}))
app.use('/v1/answers', answersRouter(answersModel))
app.use('/v1/images', imagesRouter(imagesModel))
// For unit tests
exports.app = app