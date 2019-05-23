const chai = require("chai")
const chaiHttp = require("chai-http")
const { app } = require("../app")

chai.should()
chai.use(chaiHttp)

describe('Answers tests', () => {
    
  it("should list an answer on /v1/answers/<imageName> GET", done => {
      chai
      .request(app)
      .get('/v1/answers/pachiderme')
      .end((err, res) => {
        res
          .should
          .have
          .status(200)
        res.should.be.json
        res
          .body
          .imageName
          .should
          .equal('pachiderme')
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
    
    
    
    
})