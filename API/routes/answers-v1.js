const express = require('express')
const router = express.Router()

/* GET a specific user by image name */
router.get('/:imageName', function (req, res, next) {
  const imageName = req.params.imageName

  /* istanbul ignore else */
  if (imageName) {
    try {
      const answersFound = answersModel.get(imageName)
      if (answersFound) {
        res.json(answersFound)
      } else {
        res
          .status(404)
          .json({message: `Answer not found with image name ${imageName}`})
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

/* Post a specific user by id 
router.post('/:imageName', function (req, res, next) {
  const id = req.params.id

  if (id) {
    try {
      const userFound = answerModel.post(id)
      if (userFound) {
        res.json(userFound)
      } else {
        res
          .status(404)
          .json({message: `Answer not found with image name ${imageName}`})
      }
    } catch (exc) {

      res
        .status(400)
        .json({message: exc.message})
    }

  } else {
    res
      .status(400)
      .json({message: 'Wrong parameter'})
  }
})*/

/** return a closure to initialize model */
module.exports = (model) => {
  answersModel = model
  return router
}