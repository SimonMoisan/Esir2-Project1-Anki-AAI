const answers = [
    {
        id: '987sd88a-45q6-78d8-4565-2d42b21b1a3e',
        answer: 'éléphant',
        nbrVotes: 10
    },
    {
        id: '654de540-877a-65e5-4565-2d42b21b1a3e',
        answer: 'coccinelle',
        nbrVotes: 10
    }
]

const get = (id) => {
    const answersFound = answers.filter((answers) => answers.id === id)
    return answersFound.length >= 1
        ? answersFound[0]
        : undefined
}

const add = (answer) => {
    console.log("test" + answer)
    const newAnswer = {
        ...answer
    }
    if (validateAnswer(newAnswer)) {
        answers.push(newAnswer)
    } else {
        console.log(newAnswer)
        throw new Error('image.not.valid')
    }
    console.log(newAnswer)
    return newAnswer
}


function validateAnswer(answer) {
    let result = true
    if (answer && answer.id && answer.answer && answer.nbrVotes) {
        result = true
    }
    return result
}

const getAll = () => {
    return answers
}

exports.get = get
exports.getAll = getAll
exports.add = add