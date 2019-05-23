const express = require('express')
const router = express.Router()

/* GET a specific image by id */
router.get('/:id', function (req, res, next) {
  const id = req.params.id

  /* istanbul ignore else */
  if (id) {
    try {
      const imagesFound = imagesModel.get(id)
      if (imagesFound) {
        res.json(imagesFound)
      } else {
        res
          .status(404)
          .json({message: `Image not found with image id ${id}`})
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

/* GET all images */
router.get('/', function (req, res, next) {
  res.json(imagesModel.getAll())
})

/* Add a new user. */
router.post('/', function (req, res, next) {
  const newImage = req.body

  /* istanbul ignore else */
  if (newImage) {
    try {
      const image = imagesModel.add(newImage)
      req
        .res
        .status(201)
        .send(image)
    } catch (exc) {
      res
        .status(400)
        .json({message: exc.message})
    }
  } else {
    res
      .status(400)
      .json({message: 'Wrong parameters '})
  }
})


/** return a closure to initialize model */
module.exports = (model) => {
  imagesModel = model
  return router
}