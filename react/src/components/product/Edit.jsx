import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Service from './Service'
import Util from '../../util'

export default function ProductEdit(props) {
  
  const [ product, setProduct ] = useState({})
  const [ brands, setBrands ] = useState([])
  const [ errors, setErrors ] = useState({})
  
  useEffect(() => {
    get().finally(() => {
      Util.initView(true)
    })
  }, [ props.match.params.id ])
  
  function get() {
    return Service.edit(props.match.params.id).then(response => {
      setProduct(response.data.product)
      setBrands(response.data.brands)
    }).catch(e => {
      alert(e.response.data.message)
    })
  }

  function edit(e) {
    e.preventDefault()
    let data = { ...product }
    data.imageFile = document.getElementsByName('imageFile')[0].files[0]
    data = Util.getFormData(data)
    Service.edit(props.match.params.id, data).then(() => {
      props.history.push(Util.getRef('/product'))
    }).catch((e) => {
      if (e.response.data.errors) {
        setErrors(e.response.data.errors)
      }
      else {
        alert(e.response.data.message)
      }
    })
  }

  function onChange(e) {
    let data = { ...product }
    data[e.target.name] = e.target.value
    setProduct(data)
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <form method="post" onSubmit={edit} encType="multipart/form-data">
            <div className="row">
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="product_id">Id</label>
                <input readOnly id="product_id" name="id" className="form-control form-control-sm" onChange={onChange} value={product.id ?? '' } type="number" required />
                {errors.id && <span className="text-danger">{errors.id}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="product_name">Name</label>
                <input id="product_name" name="name" className="form-control form-control-sm" onChange={onChange} value={product.name ?? '' } required maxLength="50" />
                {errors.name && <span className="text-danger">{errors.name}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="product_price">Price</label>
                <input id="product_price" name="price" className="form-control form-control-sm" onChange={onChange} value={product.price ?? '' } type="number" step="0.1" required />
                {errors.price && <span className="text-danger">{errors.price}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="product_brand_id">Brand</label>
                <select id="product_brand_id" name="brand_id" className="form-select form-select-sm" onChange={onChange} value={product.brand_id ?? '' } required>
                  <option></option>
                  {brands.map((brand, index) =>
                  <option key={index} value={brand.id}>{brand.name}</option>
                  )}
                </select>
                {errors.brand_id && <span className="text-danger">{errors.brand_id}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="product_image">Image</label>
                <input type="file" accept="image/*" id="product_image" name="imageFile" className="form-control form-control-sm" maxLength="50" />
                <a href={`http://localhost:8000/uploads/products/${product.image ?? '' }`} target="_blank" rel="noreferrer" title={`${product.image ?? '' }`}><img className="img-item" src={`http://localhost:8000/uploads/products/${product.image ?? '' }`} /></a>
                {errors.image && <span className="text-danger">{errors.image}</span>}
              </div>
              <div className="col-12">
                <Link className="btn btn-sm btn-secondary" to={Util.getRef('/product')}>Cancel</Link>
                <button className="btn btn-sm btn-primary">Submit</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}