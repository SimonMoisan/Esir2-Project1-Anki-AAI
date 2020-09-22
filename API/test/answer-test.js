const chai = require("chai")
const chaiHttp = require("chai-http")
const { app } = require("../app")

chai.should()
chai.use(chaiHttp)

describe('Answers tests', () => {
    
  it("should list an answer on /v1/answers/<imageName> GET", done => {
      chai
      .request(app)
      .get('/v1/answers/654de540-877a-65e5-4565-2d42b21b1a3e')
      .end((err, res) => {
        res
          .should
          .have
          .status(200)
        res.should.be.json
        res
          .body
          .id
          .should
          .equal('654de540-877a-65e5-4565-2d42b21b1a3e')
        done()
    })
  })
    
  it('should list ALL answers on /v1/answers GET', done => {
    chai
        .request(app)
        .get('/v1/answers')
        .end((err, res) => {
        res
            .should
            .have
            .status(200)
        res.should.be.json
        res
            .body
            .should
            .be
            .a('array')
        done()
        })
  })  
    
   it("should add a SINGLE answer on /v1/answers POST", done => {
    chai
      .request(app)
      .post('/v1/answers')
      .send({id: "45745c60-7b1a-11e8-9c9c-2d42b21b1a3e", answer:"mouche", nbrVotes:8})
      .end((err, res) => {
        res.should.have.status(201)
        res.should.be.json
        res.body.should.be.a('object')
        res.body.should.have.property('id')
        res.body.should.have.property('answer')
        res.body.should.have.property('nbrVotes')
        res.body.answer.should.equal('mouche')
        res.body.nbrVotes.should.equal(8)
        done()
      })
  })     
    
    
})