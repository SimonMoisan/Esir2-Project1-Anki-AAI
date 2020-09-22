const chai = require("chai")
const chaiHttp = require("chai-http")
const { app } = require("../app")

chai.should()
chai.use(chaiHttp)

describe('Images tests', () => {
    
  it("should list an image on /v1/images/<id> GET", done => {
      chai
      .request(app)
      .get('/v1/images/45745c60-7b1a-11e8-9c9c-2d42b21b1a3e')
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
          .equal('45745c60-7b1a-11e8-9c9c-2d42b21b1a3e')
        done()
    })
  })
    
  it('should list ALL images on /v1/images GET', done => {
    chai
        .request(app)
        .get('/v1/images')
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
    
  it("should add a SINGLE image on /v1/images POST", done => {
    chai
      .request(app)
      .post('/v1/images')
      .send({id: "654de540-877a-65e5-4565-2d42b21b1a3e",image: "data:image/jpeg;base64,/9j/patate/2Q==" })
      .end((err, res) => {
        res.should.have.status(201)
        res.should.be.json
        res.body.should.be.a('object')
        res.body.should.have.property('id')
        res.body.should.have.property('image')
        res.body.image.should.equal('data:image/jpeg;base64,/9j/patate/2Q==')
        done()
      })
  })  
    
    
})