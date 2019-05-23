const uuidv1 = require('uuid/v1')
const tcomb = require('tcomb')

const IMAGE = tcomb.struct({
    imageId: tcomb.String,
    name: tcomb.String,
    image: tcomb.String,
}, {strict: true})

const images = [
    {
        imageId:'250',
        name:'pachiderme',
        image:''
    },
    {
        imageId:'249',
        name:'girafe',
        image:''
    }
]

const get = (imageId) => {
    const imagesFound = images.filter((images) => images.imageId === imageId)
    return imagesFound.length >= 1
        ? imagesFound[0]
        : undefined
}

const add = (image) => {
    const newImage = {
        ...image,
        id: uuidv1()
    }
    if (validateImage(newImage)) {
        images.push(newImage)
    } else {
        throw new Error('user.not.valid')
    }
    return newImage
}

const getAll = () => {
    return images
}

exports.get = get
exports.getAll = getAll
exports.add = add