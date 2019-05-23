const express = require('express')
const router = express.Router()

/* GET a specific user by image name */
router.get('/:id', function (req, res, next) {
  const id = req.params.id

  /* istanbul ignore else */
  if (id) {
    try {
      const answersFound = answersModel.get(id)
      if (answersFound) {
        res.json(answersFound)
      } else {
        res
          .status(404)
          .json({message: `Answer not found with image id ${id}`})
      }
    } catch (exc) {
      /* istanbul ignore next */
      res
        .status(400)
        .json({message: exc.message})
    }

  } else {
    res
      .status(400)
      .json({message: 'Wrong parameter'})
  }
})

/* GET all users */
router.get('/', function (req, res, next) {
  res.json(answersModel.getAll())
})


/* Add a new user. */
router.post('/', function (req, res, next) {
  const newAnswer = req.body

  /* istanbul ignore else */
  if (newAnswer) {
    try {
      const answer = answersModel.add(newAnswer)
      req
        .res
        .status(201)
        .send(answer)
    } catch (exc) {
      res
        .status(400)
        .json({message: exc.message})
    }
  } else {
    res
      .status(400)
      .json({message: 'Wrong parameters ' + req.body})
  }
})

/** return a closure to initialize model */
module.exports = (model) => {
  answersModel = model
  return router
}