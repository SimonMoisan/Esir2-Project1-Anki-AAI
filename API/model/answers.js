const answers = [
    {
        imageName: 'pachiderme',
        ans: 'éléphant',
        nbrVotes: 10
    },
    {
        imageName: 'girafe',
        ans: 'coccinelle',
        nbrVotes: 10
    }
]

const get = (imageName) => {
    const answersFound = answers.filter((answers) => answers.imageName === imageName)
    return answersFound.length >= 1
        ? answersFound[0]
        : undefined
}

const getAll = () => {
    return answers
}

exports.get = get
exports.getAll = getAll