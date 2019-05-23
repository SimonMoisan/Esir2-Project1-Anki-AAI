const chai = require("chai")
const chaiHttp = require("chai-http")
const { app } = require("../app")

chai.should()
chai.use(chaiHttp)

describe('Images tests', () => {
    
  it("should list an image on /v1/images/<imageId> GET", done => {
      chai
      .request(app)
      .get('/v1/images/250')
      .end((err, res) => {
        res
          .should
          .have
          .status(200)
        res.should.be.json
        res
          .body
          .imageId
          .should
          .equal('250')
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
      .post("/v1/images")
      .send({ imageId: "251", name: "bachibouzouc", image: "" })
      .end((err, res) => {
        res.should.have.status(201)
        res.should.be.json
        res.body.should.be.a("object")
        res.body.should.have.property("imageId")
        res.body.should.have.property("name")
        res.body.imageId.should.equal("251")
        res.body.name.should.equal("bachibouzouc")
        done()
      })
  })  
    
    
})