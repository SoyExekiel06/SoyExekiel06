const express  = require('express')
const productos = require('../data/productos')

const categoriaRouter = express.Router()

categoriaRouter.post('/', (req,res) =>{
    const body = req.body
    const categorias = productos.infoProductos
    //falta codigo
    res.statusCode = 201
    res.end(JSON.stringify(body))
})

module.exports = categoriaRouter